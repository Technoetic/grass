"""
GitHub 사용자 정보 확인 도구
여러 방법으로 GitHub 사용자 정보를 확인합니다.
"""
import subprocess
import sys
from pathlib import Path


def check_gh_cli():
    """GitHub CLI로 사용자 확인"""
    try:
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            # 출력에서 사용자명 추출
            for line in result.stdout.split('\n'):
                if 'Logged in to' in line or 'as' in line.lower():
                    print(f"✅ GitHub CLI: {line.strip()}")
                    return True
        return False
    except FileNotFoundError:
        return False
    except Exception as e:
        return False


def check_git_config():
    """Git 설정에서 정보 확인"""
    try:
        # 로컬 설정 확인
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0 and result.stdout.strip():
            username = result.stdout.strip()
            print(f"📝 Git 사용자명: {username}")
            return username
    except:
        pass
    return None


def check_remote_url():
    """원격 저장소 URL에서 사용자명 추출"""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # URL에서 사용자명 추출
            if 'github.com' in url:
                parts = url.replace('https://github.com/', '').replace('git@github.com:', '').split('/')
                if len(parts) >= 1:
                    username = parts[0].replace('.git', '')
                    print(f"🔗 원격 저장소에서 발견: {username}")
                    return username
    except:
        pass
    return None


def main():
    """메인 함수"""
    print("=" * 60)
    print("GitHub 사용자 정보 확인")
    print("=" * 60)
    print()
    
    found = False
    
    # 방법 1: GitHub CLI
    print("1️⃣ GitHub CLI 확인 중...")
    if check_gh_cli():
        found = True
    else:
        print("   ❌ GitHub CLI가 설치되어 있지 않거나 로그인되지 않았습니다.")
    print()
    
    # 방법 2: Git 설정
    print("2️⃣ Git 설정 확인 중...")
    username = check_git_config()
    if username:
        found = True
        print(f"   ℹ️  이 사용자명이 GitHub 사용자명일 수도 있습니다: {username}")
    else:
        print("   ❌ Git 사용자명이 설정되어 있지 않습니다.")
    print()
    
    # 방법 3: 원격 저장소
    print("3️⃣ 원격 저장소 확인 중...")
    remote_username = check_remote_url()
    if remote_username:
        found = True
    else:
        print("   ❌ 원격 저장소가 설정되어 있지 않습니다.")
    print()
    
    print("=" * 60)
    if not found:
        print("❌ 자동으로 GitHub 사용자명을 찾을 수 없습니다.")
        print()
        print("다음 중 하나를 시도하세요:")
        print("1. GitHub 웹사이트에서 확인:")
        print("   - https://github.com 접속")
        print("   - 우측 상단 프로필 클릭")
        print("   - 사용자명 확인")
        print()
        print("2. Cursor에서 확인:")
        print("   - Ctrl + Shift + P")
        print("   - 'GitHub: Show Account' 입력")
        print()
        print("3. 직접 알려주세요:")
        print("   GitHub 사용자명을 알려주시면 바로 연결하겠습니다!")
    else:
        print("✅ 정보를 찾았습니다!")
        print()
        print("원격 저장소를 설정하려면:")
        if username:
            print(f"  git remote add origin https://github.com/{username}/grass.git")
            print(f"  git push -u origin master")


if __name__ == '__main__':
    main()


