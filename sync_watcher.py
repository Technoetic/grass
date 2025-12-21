"""
로컬 폴더와 Git 저장소 실시간 동기화
파일이 변경되면 자동으로 커밋하고 GitHub에 푸시합니다.
"""
import os
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Set

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
except ImportError:
    print("❌ watchdog 모듈이 설치되어 있지 않습니다.")
    print("   설치: pip install watchdog")
    sys.exit(1)


class SyncHandler(FileSystemEventHandler):
    """파일 변경 이벤트 핸들러"""
    
    def __init__(self, auto_push: bool = True, debounce_seconds: int = 5):
        """
        초기화
        
        Args:
            auto_push: 자동 푸시 여부
            debounce_seconds: 디바운스 시간 (초)
        """
        self.auto_push = auto_push
        self.debounce_seconds = debounce_seconds
        self.last_commit_time = 0
        self.pending_changes = set()
        self.sync_timer = None
        self.ignored_patterns = {
            '.git', '__pycache__', '.pyc', '.pyo', '.pyd',
            '.log', '.tmp', '.swp', '.swo', '~'
        }
        self.ignored_dirs = {'.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules'}
        
    def should_ignore(self, path: str) -> bool:
        """파일/디렉토리를 무시할지 확인"""
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
            if path_obj.name.startswith('.'):
                return True
        
        return False
    
    def on_modified(self, event: FileSystemEvent):
        """파일 수정 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            print(f"📝 [{datetime.now().strftime('%H:%M:%S')}] 파일 변경 감지: {Path(event.src_path).name}")
            self.pending_changes.add(event.src_path)
            self.schedule_sync()
    
    def on_created(self, event: FileSystemEvent):
        """파일 생성 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            print(f"➕ [{datetime.now().strftime('%H:%M:%S')}] 파일 생성 감지: {Path(event.src_path).name}")
            self.pending_changes.add(event.src_path)
            self.schedule_sync()
    
    def on_deleted(self, event: FileSystemEvent):
        """파일 삭제 이벤트"""
        if not event.is_directory and not self.should_ignore(event.src_path):
            print(f"➖ [{datetime.now().strftime('%H:%M:%S')}] 파일 삭제 감지: {Path(event.src_path).name}")
            self.pending_changes.add(event.src_path)
            self.schedule_sync()
    
    def schedule_sync(self):
        """동기화 스케줄링 (디바운스)"""
        # 디바운스를 위해 타이머 사용
        if not hasattr(self, 'sync_timer'):
            self.sync_timer = None
        
        # 기존 타이머 취소
        if self.sync_timer:
            self.sync_timer.cancel()
        
        # 새 타이머 설정
        import threading
        def delayed_sync():
            time.sleep(self.debounce_seconds)
            if self.pending_changes:
                self.sync_changes()
            self.sync_timer = None
        
        self.sync_timer = threading.Timer(self.debounce_seconds, delayed_sync)
        self.sync_timer.daemon = True
        self.sync_timer.start()
    
    def sync_changes(self):
        """변경사항 동기화 (커밋 + 푸시)"""
        try:
            # Git 상태 확인
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if not status_result.stdout.strip():
                self.pending_changes.clear()
                return
            
            changed_files = [line for line in status_result.stdout.strip().split('\n') if line.strip()]
            
            # 파일 추가
            subprocess.run(
                ['git', 'add', '.'],
                check=True,
                capture_output=True
            )
            
            # 커밋 메시지 생성
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file_names = [Path(f.split()[-1]).name for f in changed_files[:5]]
            if len(changed_files) > 5:
                file_names.append(f"외 {len(changed_files) - 5}개")
            
            commit_message = f"자동 동기화: {', '.join(file_names)} ({timestamp})"
            
            # 커밋
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if commit_result.returncode == 0:
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] 커밋 완료: {commit_message}")
                
                # 푸시
                if self.auto_push:
                    push_result = subprocess.run(
                        ['git', 'push'],
                        capture_output=True,
                        text=True,
                        encoding='utf-8'
                    )
                    
                    if push_result.returncode == 0:
                        # 브랜치 정보 가져오기
                        branch_result = subprocess.run(
                            ['git', 'branch', '--show-current'],
                            capture_output=True,
                            text=True,
                            encoding='utf-8'
                        )
                        branch_name = branch_result.stdout.strip() if branch_result.returncode == 0 else '알 수 없음'
                        
                        # 원격 저장소 정보 가져오기
                        remote_result = subprocess.run(
                            ['git', 'remote', 'get-url', 'origin'],
                            capture_output=True,
                            text=True,
                            encoding='utf-8'
                        )
                        remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else '알 수 없음'
                        
                        # 최근 커밋 해시 가져오기
                        commit_hash_result = subprocess.run(
                            ['git', 'log', '-1', '--format=%h'],
                            capture_output=True,
                            text=True,
                            encoding='utf-8'
                        )
                        commit_hash = commit_hash_result.stdout.strip() if commit_hash_result.returncode == 0 else ''
                        
                        # 상세한 푸시 확인 메시지 출력
                        print()
                        print("=" * 60)
                        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Git Push 완료!")
                        print("=" * 60)
                        print(f"📦 브랜치: {branch_name}")
                        print(f"🔗 원격 저장소: {remote_url}")
                        if commit_hash:
                            print(f"📝 커밋 해시: {commit_hash}")
                        print(f"⏰ 푸시 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print("=" * 60)
                        print()
                    else:
                        print(f"⚠️  [{datetime.now().strftime('%H:%M:%S')}] 푸시 실패: {push_result.stderr}")
            else:
                print(f"ℹ️  [{datetime.now().strftime('%H:%M:%S')}] {commit_result.stderr}")
            
            self.pending_changes.clear()
            self.last_commit_time = time.time()
            if hasattr(self, 'sync_timer') and self.sync_timer:
                self.sync_timer.cancel()
                self.sync_timer = None
            
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 동기화 오류: {e}")
            import traceback
            traceback.print_exc()


class SyncWatcher:
    """실시간 동기화 감시자"""
    
    def __init__(self, repo_path: Optional[str] = None, auto_push: bool = True, debounce: int = 5):
        """
        초기화
        
        Args:
            repo_path: 감시할 디렉토리 경로
            auto_push: 자동 푸시 여부
            debounce: 디바운스 시간 (초)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.auto_push = auto_push
        self.debounce = debounce
        self.observer = None
        
    def start(self):
        """감시 시작"""
        print("=" * 60)
        print("🔄 실시간 동기화 시작")
        print("=" * 60)
        print(f"📁 감시 디렉토리: {self.repo_path}")
        print(f"⏱️  디바운스 시간: {self.debounce}초")
        print(f"🚀 자동 푸시: {'사용' if self.auto_push else '사용 안 함'}")
        print("=" * 60)
        print("💡 중지하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        print()
        
        # 이벤트 핸들러 생성
        event_handler = SyncHandler(auto_push=self.auto_push, debounce_seconds=self.debounce)
        
        # 옵저버 생성 및 시작
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.repo_path), recursive=True)
        self.observer.start()
        
        try:
            # 감시 루프
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  동기화 중지 중...")
            self.stop()
    
    def stop(self):
        """감시 중지"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("✅ 동기화 중지 완료")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='로컬 폴더와 Git 저장소 실시간 동기화',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예제:
  python sync_watcher.py
  python sync_watcher.py --no-push
  python sync_watcher.py --debounce 10
        """
    )
    
    parser.add_argument('--path', '-p', help='감시할 디렉토리 경로 (기본: 현재 디렉토리)')
    parser.add_argument('--no-push', action='store_true', help='자동 푸시 비활성화')
    parser.add_argument('--debounce', type=int, default=5, help='디바운스 시간 (초, 기본: 5)')
    
    args = parser.parse_args()
    
    watcher = SyncWatcher(
        repo_path=args.path,
        auto_push=not args.no_push,
        debounce=args.debounce
    )
    
    watcher.start()


if __name__ == '__main__':
    main()

