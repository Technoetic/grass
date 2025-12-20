"""
Cursor IDE의 GitHub 통합을 활용한 저장소 설정
Cursor가 GitHub에 로그인되어 있다면 이를 활용합니다.
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


def check_cursor_github_integration():
    """Cursor의 GitHub 통합 확인"""
    print("=" * 60)
    print("Cursor IDE GitHub 통합 확인")
    print("=" * 60)
    print()
    print("Cursor IDE에서 GitHub 계정이 로그인되어 있다면,")
    print("다음 방법으로 저장소를 설정할 수 있습니다:")
    print()
    print("1. Cursor의 소스 제어 패널 사용")
    print("   - Ctrl + Shift + G (소스 제어 열기)")
    print("   - '...' 메뉴 클릭")
    print("   - 'Publish to GitHub' 선택")
    print("   - 저장소 이름 입력 후 생성")
    print()
    print("2. GitHub 웹사이트에서 저장소 생성 후 연결")
    print("   - https://github.com/new 접속")
    print("   - 저장소 생성")
    print("   - 아래 명령어로 연결")
    print()


def setup_remote_from_cursor():
    """Cursor의 GitHub 통합을 통한 원격 저장소 설정"""
    print("=" * 60)
    print("GitHub 저장소 설정")
    print("=" * 60)
    print()
    
    # 현재 원격 저장소 확인
    success, output = run_command(['git', 'remote', '-v'])
    if output:
        print("현재 원격 저장소:")
        print(output)
        print()
        return
    
    print("원격 저장소가 설정되어 있지 않습니다.")
    print()
    print("Cursor IDE에서 GitHub에 로그인되어 있다면,")
    print("다음 중 하나를 선택하세요:")
    print()
    print("옵션 1: Cursor UI 사용 (가장 쉬움)")
    print("  1. Ctrl + Shift + G (소스 제어 패널)")
    print("  2. '...' 메뉴 클릭")
    print("  3. 'Publish to GitHub' 선택")
    print("  4. 저장소 이름 입력 (예: grass)")
    print("  5. Public/Private 선택")
    print("  6. 'Publish' 클릭")
    print()
    print("옵션 2: 수동으로 원격 저장소 추가")
    print("  GitHub 저장소 URL을 알려주시면 연결하겠습니다.")
    print()
    
    # GitHub 사용자명 확인 시도
    print("GitHub 사용자명을 입력하세요 (또는 Enter로 건너뛰기): ", end='')
    # username = input().strip()
    username = ""
    
    if username:
        repo_name = "grass"  # 기본값
        print(f"\n저장소 이름 (기본: {repo_name}): ", end='')
        # repo_name_input = input().strip()
        # if repo_name_input:
        #     repo_name = repo_name_input
        
        url = f"https://github.com/{username}/{repo_name}.git"
        print(f"\n원격 저장소 추가: {url}")
        
        success, output = run_command(['git', 'remote', 'add', 'origin', url])
        if success:
            print("✅ 원격 저장소 추가 완료!")
            print(f"\n다음 단계:")
            print(f"  git push -u origin master")
        else:
            print(f"❌ 실패: {output}")
    else:
        print("\n수동 설정 방법:")
        print("  git remote add origin https://github.com/your-username/grass.git")
        print("  git push -u origin master")


def main():
    """메인 함수"""
    check_cursor_github_integration()
    setup_remote_from_cursor()


if __name__ == '__main__':
    main()


