"""
Cursor IDE의 GitHub 계정 정보 확인
Cursor가 GitHub에 로그인되어 있다면 계정 정보를 찾아봅니다.
"""
import os
import json
import subprocess
from pathlib import Path


def check_cursor_settings():
    """Cursor 설정 파일에서 GitHub 정보 확인"""
    app_data = os.getenv('APPDATA')
    settings_path = Path(app_data) / 'Cursor' / 'User' / 'settings.json'
    
    if settings_path.exists():
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # GitHub 관련 설정 찾기
            github_settings = {}
            for key, value in settings.items():
                if 'github' in key.lower():
                    github_settings[key] = value
            
            return github_settings, settings
        except Exception as e:
            print(f"설정 파일 읽기 오류: {e}")
    
    return {}, None


def check_git_credential_manager():
    """Git Credential Manager에서 GitHub 정보 확인"""
    try:
        # Windows Credential Manager 확인
        result = subprocess.run(
            ['cmdkey', '/list'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'github' in line.lower():
                    return line.strip()
    except:
        pass
    return None


def check_github_cli():
    """GitHub CLI로 계정 확인"""
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
                    return result.stdout
    except FileNotFoundError:
        return None
    except:
        return None
    return None


def check_git_config():
    """Git 설정에서 정보 확인"""
    try:
        result = subprocess.run(
            ['git', 'config', '--global', '--list'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            config = {}
            for line in result.stdout.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if 'github' in key.lower() or 'user' in key.lower():
                        config[key] = value
            return config
    except:
        pass
    return {}


def main():
    """메인 함수"""
    print("=" * 60)
    print("Cursor IDE GitHub 계정 정보 확인")
    print("=" * 60)
    print()
    
    found_info = False
    
    # 방법 1: Cursor 설정 파일
    print("1️⃣ Cursor 설정 파일 확인 중...")
    github_settings, all_settings = check_cursor_settings()
    if github_settings:
        print("   ✅ GitHub 관련 설정 발견:")
        for key, value in github_settings.items():
            print(f"      {key}: {value}")
        found_info = True
    else:
        print("   ❌ Cursor 설정에서 GitHub 정보를 찾을 수 없습니다.")
    print()
    
    # 방법 2: GitHub CLI
    print("2️⃣ GitHub CLI 확인 중...")
    gh_status = check_github_cli()
    if gh_status:
        print("   ✅ GitHub CLI 정보:")
        print(f"      {gh_status}")
        found_info = True
    else:
        print("   ❌ GitHub CLI가 설치되어 있지 않거나 로그인되지 않았습니다.")
    print()
    
    # 방법 3: Git 설정
    print("3️⃣ Git 설정 확인 중...")
    git_config = check_git_config()
    if git_config:
        print("   ✅ Git 설정:")
        for key, value in git_config.items():
            print(f"      {key}: {value}")
        found_info = True
    else:
        print("   ❌ Git 설정에서 GitHub 정보를 찾을 수 없습니다.")
    print()
    
    # 방법 4: Credential Manager
    print("4️⃣ Windows Credential Manager 확인 중...")
    cred = check_git_credential_manager()
    if cred:
        print(f"   ✅ 발견: {cred}")
        found_info = True
    else:
        print("   ❌ Credential Manager에서 GitHub 정보를 찾을 수 없습니다.")
    print()
    
    print("=" * 60)
    if not found_info:
        print("❌ 자동으로 GitHub 계정 정보를 찾을 수 없습니다.")
        print()
        print("Cursor IDE의 GitHub 로그인 정보는 보안상의 이유로")
        print("일반적인 방법으로는 접근할 수 없습니다.")
        print()
        print("다음 방법을 사용하세요:")
        print()
        print("방법 1: Cursor에서 직접 확인")
        print("  1. Ctrl + Shift + P")
        print("  2. 'GitHub: Show Account' 입력")
        print("  3. 계정 정보 확인")
        print()
        print("방법 2: Cursor의 'Publish to GitHub' 사용")
        print("  - 사용자명을 입력할 필요 없이 자동으로 처리됩니다")
        print("  - Ctrl + Shift + G → '...' → 'Publish to GitHub'")
        print()
        print("방법 3: GitHub 웹사이트에서 확인")
        print("  - https://github.com 접속")
        print("  - 우측 상단 프로필에서 사용자명 확인")
    else:
        print("✅ 일부 정보를 찾았습니다!")
        print()
        print("하지만 Cursor의 GitHub 로그인 정보는")
        print("보안상의 이유로 직접 접근할 수 없습니다.")
        print()
        print("가장 쉬운 방법:")
        print("  Cursor의 'Publish to GitHub' 기능을 사용하세요!")
        print("  (사용자명을 입력할 필요 없음)")


if __name__ == '__main__':
    main()

