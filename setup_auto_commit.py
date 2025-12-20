"""
자동 커밋 설정 도구
코드 실행 시 자동으로 커밋되도록 설정합니다.
"""
import os
import sys
from pathlib import Path


def create_runner_script():
    """실행 스크립트 생성"""
    runner_content = '''@echo off
REM 자동 커밋 실행 스크립트
python auto_commit_on_run.py %*
'''
    
    runner_path = Path('run.bat')
    with open(runner_path, 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    print(f"✅ {runner_path} 생성 완료!")
    return runner_path


def setup_git_hooks():
    """Git hooks 설정 (선택사항)"""
    hooks_dir = Path('.git/hooks')
    
    if not hooks_dir.exists():
        print("⚠️  Git 저장소가 아닙니다.")
        return False
    
    # post-commit hook 예제 (참고용)
    post_commit_hook = hooks_dir / 'post-commit'
    hook_content = '''#!/bin/sh
# 자동 푸시 (선택사항)
# git push
'''
    
    print("💡 Git hooks는 수동으로 설정할 수 있습니다.")
    return True


def main():
    """메인 함수"""
    print("=" * 60)
    print("자동 커밋 설정")
    print("=" * 60)
    print()
    
    # Windows용 실행 스크립트 생성
    if os.name == 'nt':
        create_runner_script()
        print()
        print("사용 방법:")
        print("  run.bat 251220.py")
        print("  또는")
        print("  python run.py 251220.py")
    else:
        print("사용 방법:")
        print("  python run.py 251220.py")
        print("  또는")
        print("  python auto_commit_on_run.py 251220.py")
    
    print()
    print("=" * 60)
    print("설정 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()

