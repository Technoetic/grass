"""
간편 실행 스크립트
코드를 실행하면 자동으로 커밋됩니다.
"""
import sys
import subprocess
from pathlib import Path


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python run.py <스크립트.py> [인자들...]")
        print()
        print("예제:")
        print("  python run.py 251220.py")
        sys.exit(1)
    
    script = sys.argv[1]
    args = sys.argv[2:]
    
    # auto_commit_on_run.py를 통해 실행
    cmd = [sys.executable, 'auto_commit_on_run.py', script] + args
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


if __name__ == '__main__':
    main()

