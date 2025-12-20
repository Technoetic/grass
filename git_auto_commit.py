"""
Git 자동 커밋 도구
Cursor IDE의 Git 통합을 활용하여 실제 활동을 자동으로 커밋합니다.
"""
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict


class GitAutoCommit:
    """Git 자동 커밋 관리 클래스"""
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Git 자동 커밋 초기화
        
        Args:
            repo_path: Git 저장소 경로 (없으면 현재 디렉토리)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_dir = self.repo_path / '.git'
        
        if not self.git_dir.exists():
            raise ValueError(f"Git 저장소가 아닙니다: {self.repo_path}")
    
    def _run_git(self, *args) -> tuple[str, str, int]:
        """
        Git 명령어 실행
        
        Args:
            *args: Git 명령어 인자들
            
        Returns:
            (stdout, stderr, returncode) 튜플
        """
        cmd = ['git'] + list(args)
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    
    def check_status(self) -> Dict:
        """
        Git 저장소 상태 확인
        
        Returns:
            상태 정보 딕셔너리
        """
        stdout, stderr, code = self._run_git('status', '--porcelain')
        changed_files = [line for line in stdout.split('\n') if line.strip()]
        
        stdout, _, _ = self._run_git('status', '--short', '--branch')
        branch_info = stdout.split('\n')[0] if stdout else ''
        
        return {
            'has_changes': len(changed_files) > 0,
            'changed_files': changed_files,
            'branch': branch_info,
            'count': len(changed_files)
        }
    
    def get_branch(self) -> str:
        """
        현재 브랜치 이름 가져오기
        
        Returns:
            브랜치 이름
        """
        stdout, _, _ = self._run_git('branch', '--show-current')
        return stdout.strip() or 'main'
    
    def add_files(self, files: Optional[List[str]] = None) -> bool:
        """
        파일을 스테이징 영역에 추가
        
        Args:
            files: 추가할 파일 목록 (None이면 모든 변경사항)
            
        Returns:
            성공 여부
        """
        if files:
            for file in files:
                _, _, code = self._run_git('add', file)
                if code != 0:
                    return False
        else:
            _, _, code = self._run_git('add', '.')
            if code != 0:
                return False
        return True
    
    def commit(self, message: Optional[str] = None, 
               allow_empty: bool = False) -> bool:
        """
        커밋 생성
        
        Args:
            message: 커밋 메시지 (없으면 자동 생성)
            allow_empty: 빈 커밋 허용 여부
            
        Returns:
            성공 여부
        """
        if not message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"Update: {timestamp}"
        
        cmd = ['commit', '-m', message]
        if allow_empty:
            cmd.append('--allow-empty')
        
        _, stderr, code = self._run_git(*cmd)
        return code == 0
    
    def push(self, remote: str = 'origin', branch: Optional[str] = None) -> bool:
        """
        원격 저장소에 푸시
        
        Args:
            remote: 원격 저장소 이름
            branch: 브랜치 이름 (없으면 현재 브랜치)
            
        Returns:
            성공 여부
        """
        if not branch:
            branch = self.get_branch()
        
        _, stderr, code = self._run_git('push', remote, branch)
        return code == 0
    
    def auto_commit(self, message: Optional[str] = None, 
                   push: bool = False) -> Dict:
        """
        자동 커밋 수행 (변경사항이 있을 때만)
        
        Args:
            message: 커밋 메시지
            push: 푸시 여부
            
        Returns:
            실행 결과 딕셔너리
        """
        status = self.check_status()
        
        if not status['has_changes']:
            return {
                'success': False,
                'message': '커밋할 변경사항이 없습니다.',
                'status': status
            }
        
        # 파일 추가
        if not self.add_files():
            return {
                'success': False,
                'message': '파일 추가 실패',
                'status': status
            }
        
        # 커밋
        if not self.commit(message):
            return {
                'success': False,
                'message': '커밋 실패',
                'status': status
            }
        
        result = {
            'success': True,
            'message': '커밋 성공',
            'status': status,
            'committed_files': status['changed_files']
        }
        
        # 푸시
        if push:
            if self.push():
                result['pushed'] = True
                result['message'] = '커밋 및 푸시 성공'
            else:
                result['pushed'] = False
                result['message'] = '커밋 성공, 푸시 실패'
        
        return result
    
    def get_recent_commits(self, count: int = 5) -> List[Dict]:
        """
        최근 커밋 목록 가져오기
        
        Args:
            count: 가져올 커밋 수
            
        Returns:
            커밋 목록
        """
        stdout, _, _ = self._run_git(
            'log',
            f'-{count}',
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=iso'
        )
        
        commits = []
        for line in stdout.split('\n'):
            if not line.strip():
                continue
            parts = line.split('|', 4)
            if len(parts) == 5:
                commits.append({
                    'hash': parts[0][:7],
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3],
                    'message': parts[4]
                })
        
        return commits


def main():
    """메인 함수 - 간단한 사용 예제"""
    print("Git 자동 커밋 도구\n")
    
    try:
        git = GitAutoCommit()
        
        # 상태 확인
        status = git.check_status()
        branch = git.get_branch()
        
        print(f"📍 저장소: {git.repo_path}")
        print(f"🌿 브랜치: {branch}")
        print(f"📊 변경사항: {status['count']}개 파일\n")
        
        if status['has_changes']:
            print("변경된 파일:")
            for file in status['changed_files'][:10]:
                print(f"  - {file}")
            if len(status['changed_files']) > 10:
                print(f"  ... 외 {len(status['changed_files']) - 10}개")
            
            print("\n자동 커밋을 수행하시겠습니까? (y/n): ", end='')
            # 실제 사용 시에는 input() 사용
            # choice = input().strip().lower()
            # if choice == 'y':
            #     result = git.auto_commit(push=False)
            #     print(f"\n✅ {result['message']}")
        else:
            print("✅ 커밋할 변경사항이 없습니다.")
        
        # 최근 커밋 보기
        print("\n📜 최근 커밋:")
        commits = git.get_recent_commits(3)
        for commit in commits:
            print(f"  {commit['hash']} - {commit['message']}")
            print(f"    {commit['date']} by {commit['author']}")
        
    except ValueError as e:
        print(f"❌ 오류: {e}")
        print("\n현재 디렉토리를 Git 저장소로 초기화하시겠습니까?")
        print("  git init")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == '__main__':
    main()


