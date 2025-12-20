"""
실시간 파일 변경 감지 및 자동 커밋 도구
파일이 변경되면 자동으로 Git 커밋을 수행합니다.
"""
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from git_auto_commit import GitAutoCommit


class AutoCommitHandler(FileSystemEventHandler):
    """파일 변경 이벤트 핸들러"""
    
    def __init__(self, git: GitAutoCommit, config: dict):
        """
        초기화
        
        Args:
            git: GitAutoCommit 인스턴스
            config: 설정 딕셔너리
        """
        self.git = git
        self.config = config
        self.ignored_patterns = set(config.get('ignore_patterns', []))
        self.ignored_dirs = set(config.get('ignore_dirs', ['.git', '__pycache__', 'venv', 'env', '.venv']))
        self.last_commit_time = 0
        self.debounce_seconds = config.get('debounce_seconds', 5)  # 5초 디바운스
        self.pending_changes = set()
        
    def should_ignore(self, path: str) -> bool:
        """
        파일/디렉토리를 무시할지 확인
        
        Args:
            path: 파일/디렉토리 경로
            
        Returns:
            무시 여부
        """
        path_obj = Path(path)
        
        # 디렉토리 이름 확인
        for part in path_obj.parts:
            if part in self.ignored_dirs:
                return True
        
        # 파일 확장자 확인
        if path_obj.is_file():
            suffix = path_obj.suffix
            if suffix in self.ignored_patterns:
                return True
            
            # 전체 파일명 패턴 확인
            filename = path_obj.name
            for pattern in self.ignored_patterns:
                if pattern in filename or filename.endswith(pattern):
                    return True
        
        return False
    
    def on_modified(self, event: FileSystemEvent):
        """파일 수정 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.pending_changes.add(event.src_path)
            self.schedule_commit()
    
    def on_created(self, event: FileSystemEvent):
        """파일 생성 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.pending_changes.add(event.src_path)
            self.schedule_commit()
    
    def on_deleted(self, event: FileSystemEvent):
        """파일 삭제 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self.pending_changes.add(event.src_path)
            self.schedule_commit()
    
    def schedule_commit(self):
        """커밋 스케줄링 (디바운스)"""
        current_time = time.time()
        
        # 디바운스 시간이 지나지 않았으면 대기
        if current_time - self.last_commit_time < self.debounce_seconds:
            return
        
        # 변경사항이 있으면 커밋
        if self.pending_changes:
            self.commit_changes()
    
    def commit_changes(self):
        """변경사항 커밋"""
        try:
            status = self.git.check_status()
            
            if not status['has_changes']:
                self.pending_changes.clear()
                return
            
            # 커밋 메시지 생성
            if self.config.get('auto_message', True):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                changed_files = [Path(f).name for f in status['changed_files'][:5]]
                if len(status['changed_files']) > 5:
                    changed_files.append(f"외 {len(status['changed_files']) - 5}개")
                message = f"자동 커밋: {', '.join(changed_files)} ({timestamp})"
            else:
                message = self.config.get('commit_message', '자동 커밋')
            
            # 커밋 수행
            result = self.git.auto_commit(message=message, push=self.config.get('auto_push', False))
            
            if result['success']:
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] 자동 커밋 완료: {message}")
                if self.config.get('auto_push', False) and result.get('pushed'):
                    print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] 푸시 완료")
            else:
                print(f"ℹ️  [{datetime.now().strftime('%H:%M:%S')}] {result['message']}")
            
            self.pending_changes.clear()
            self.last_commit_time = time.time()
            
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 커밋 오류: {e}")


class AutoCommitWatcher:
    """실시간 자동 커밋 감시자"""
    
    def __init__(self, repo_path: Optional[str] = None, config_path: str = 'config.json'):
        """
        초기화
        
        Args:
            repo_path: Git 저장소 경로
            config_path: 설정 파일 경로
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.git = GitAutoCommit(str(self.repo_path))
        self.observer = None
        
    def load_config(self) -> dict:
        """설정 파일 로드"""
        default_config = {
            'auto_message': True,
            'auto_push': False,
            'debounce_seconds': 5,
            'ignore_patterns': ['.pyc', '.pyo', '.pyd', '.log', '.tmp'],
            'ignore_dirs': ['.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules']
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    if 'watcher' in user_config:
                        default_config.update(user_config['watcher'])
            except Exception as e:
                print(f"⚠️  설정 파일 로드 실패: {e}")
        
        return default_config
    
    def start(self):
        """감시 시작"""
        print("=" * 60)
        print("🔄 실시간 자동 커밋 감시 시작")
        print("=" * 60)
        print(f"📁 감시 디렉토리: {self.repo_path}")
        print(f"⏱️  디바운스 시간: {self.config['debounce_seconds']}초")
        print(f"📝 자동 메시지: {'사용' if self.config['auto_message'] else '사용 안 함'}")
        print(f"🚀 자동 푸시: {'사용' if self.config['auto_push'] else '사용 안 함'}")
        print(f"🚫 무시 패턴: {', '.join(self.config['ignore_patterns'][:5])}")
        print("=" * 60)
        print("💡 중지하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        print()
        
        # 이벤트 핸들러 생성
        event_handler = AutoCommitHandler(self.git, self.config)
        
        # 옵저버 생성 및 시작
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.repo_path), recursive=True)
        self.observer.start()
        
        try:
            # 감시 루프
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  감시 중지 중...")
            self.stop()
    
    def stop(self):
        """감시 중지"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("✅ 감시 중지 완료")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='실시간 파일 변경 감지 및 자동 커밋',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예제:
  python auto_commit_watcher.py
  python auto_commit_watcher.py --push
  python auto_commit_watcher.py --debounce 10
  python auto_commit_watcher.py --no-auto-message
        """
    )
    
    parser.add_argument('--path', '-p', help='감시할 디렉토리 경로 (기본: 현재 디렉토리)')
    parser.add_argument('--config', '-c', default='config.json', help='설정 파일 경로')
    parser.add_argument('--push', action='store_true', help='자동 푸시 활성화')
    parser.add_argument('--debounce', type=int, help='디바운스 시간 (초)')
    parser.add_argument('--no-auto-message', action='store_true', help='자동 메시지 비활성화')
    parser.add_argument('--message', '-m', help='고정 커밋 메시지 (--no-auto-message와 함께 사용)')
    
    args = parser.parse_args()
    
    # 설정 오버라이드
    watcher = AutoCommitWatcher(repo_path=args.path, config_path=args.config)
    
    if args.push:
        watcher.config['auto_push'] = True
    if args.debounce:
        watcher.config['debounce_seconds'] = args.debounce
    if args.no_auto_message:
        watcher.config['auto_message'] = False
    if args.message:
        watcher.config['commit_message'] = args.message
        watcher.config['auto_message'] = False
    
    # 감시 시작
    watcher.start()


if __name__ == '__main__':
    main()

