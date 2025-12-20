"""
Git 저장소 초기화 도우미
현재 디렉토리를 Git 저장소로 초기화하고 GitHub와 연동합니다.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, cwd: Path = None) -> tuple[bool, str]:
    """명령어 실행"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def init_git_repo():
    """Git 저장소 초기화"""
    current_dir = Path.cwd()
    git_dir = current_dir / '.git'
    
    if git_dir.exists():
        print("✅ 이미 Git 저장소입니다.")
        return True
    
    print(f"📁 디렉토리: {current_dir}")
    print("🔧 Git 저장소 초기화 중...")
    
    success, output = run_command(['git', 'init'], current_dir)
    if success:
        print("✅ Git 저장소 초기화 완료!")
        
        # .gitignore가 없으면 생성
        gitignore = current_dir / '.gitignore'
        if not gitignore.exists():
            print("📝 .gitignore 파일 생성 중...")
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write("""# Python
__pycache__/
*.py[cod]
*.pyc
.env
venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
""")
            print("✅ .gitignore 생성 완료!")
        
        return True
    else:
        print(f"❌ 초기화 실패: {output}")
        return False


def setup_remote():
    """원격 저장소 설정"""
    print("\n🌐 원격 저장소 설정")
    print("GitHub 저장소 URL을 입력하세요 (예: https://github.com/username/repo.git)")
    print("또는 Enter를 눌러 건너뛰세요: ", end='')
    
    # 실제 사용 시에는 input() 사용
    # url = input().strip()
    # if url:
    #     success, output = run_command(['git', 'remote', 'add', 'origin', url])
    #     if success:
    #         print(f"✅ 원격 저장소 추가: {url}")
    #     else:
    #         print(f"❌ 실패: {output}")
    # else:
    print("(건너뛰기)")


def main():
    """메인 함수"""
    print("=" * 50)
    print("Git 저장소 초기화 도우미")
    print("=" * 50)
    print()
    
    if not init_git_repo():
        sys.exit(1)
    
    setup_remote()
    
    print("\n✅ 설정 완료!")
    print("\n다음 단계:")
    print("  1. 파일을 수정하세요")
    print("  2. python commit_helper.py commit -m '메시지'")
    print("  3. python commit_helper.py commit --push (푸시)")


if __name__ == '__main__':
    main()

