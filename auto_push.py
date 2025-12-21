"""
자동 Git 커밋 및 푸시 모듈
스크립트 실행 후 자동으로 커밋하고 푸시하는 기능을 제공합니다.
"""
# __pycache__ 디렉토리 생성 방지 - 가장 먼저 실행되어야 함
import sys
import os
import shutil
import atexit
from pathlib import Path

# Python 인터프리터 레벨에서 바이트코드 생성 비활성화
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def _cleanup_pycache():
    """__pycache__ 디렉토리를 정리합니다."""
    try:
        current_dir = Path(__file__).parent
        pycache_dir = current_dir / '__pycache__'
        if pycache_dir.exists():
            shutil.rmtree(pycache_dir)
    except Exception:
        pass

# 모듈 로드 시 즉시 정리
_cleanup_pycache()

# 프로그램 종료 시에도 정리 (atexit에 등록)
atexit.register(_cleanup_pycache)

import subprocess
import atexit
import inspect
from datetime import datetime


def auto_commit_and_push(script_name: str = None, silent: bool = False) -> bool:
    """
    변경사항을 자동으로 커밋하고 푸시합니다.
    
    Args:
        script_name: 실행한 스크립트 이름 (커밋 메시지에 사용)
        silent: True이면 메시지를 출력하지 않음
    
    Returns:
        bool: 푸시 성공 여부
    """
    try:
        # Git 상태 확인
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if not status_result.stdout.strip():
            if not silent:
                print()
                print("=" * 60)
                print(f"ℹ️  [{datetime.now().strftime('%H:%M:%S')}] 커밋할 변경사항이 없습니다.")
                print("=" * 60)
            return True
        
        # 변경사항이 있으면 커밋
        subprocess.run(
            ['git', 'add', '.'],
            check=True,
            capture_output=True
        )
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if script_name:
            commit_message = f"자동 커밋: {script_name} 실행 ({timestamp})"
        else:
            commit_message = f"자동 커밋 ({timestamp})"
        
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if commit_result.returncode != 0:
            if not silent:
                print(f"⚠️  커밋 실패: {commit_result.stderr}")
            return False
        
        # 푸시 수행
        push_result = subprocess.run(
            ['git', 'push'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if push_result.returncode == 0:
            if not silent:
                _print_push_confirmation()
            return True
        else:
            if not silent:
                print(f"⚠️  푸시 실패: {push_result.stderr}")
            return False
            
    except Exception as e:
        if not silent:
            print(f"❌ Git 오류: {e}")
        return False


def _print_push_confirmation():
    """푸시 확인 메시지를 출력합니다."""
    try:
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
    except Exception:
        # 정보를 가져오지 못해도 기본 메시지 출력
        print()
        print("=" * 60)
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Git Push 완료!")
        print("=" * 60)


def _get_calling_script_name() -> str:
    """호출한 스크립트의 이름을 가져옵니다."""
    try:
        # 호출 스택을 확인하여 __main__ 모듈의 파일명을 찾음
        frame = inspect.currentframe()
        while frame:
            if frame.f_globals.get('__name__') == '__main__':
                script_path = frame.f_globals.get('__file__', '')
                if script_path:
                    return Path(script_path).name
            frame = frame.f_back
        return None
    except Exception:
        return None


def _auto_push_on_exit():
    """프로그램 종료 시 자동으로 push합니다."""
    script_name = _get_calling_script_name()
    auto_commit_and_push(script_name=script_name)


# 모듈이 import될 때 자동으로 프로그램 종료 시 push하도록 등록
atexit.register(_auto_push_on_exit)

