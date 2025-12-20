"""
로컬 커밋을 GitHub로 전송하는 도구
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, cwd: Path = None) -> tuple[bool, str, str]:
    """명령어 실행"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def check_remote():
    """원격 저장소 확인"""
    success, stdout, _ = run_command(['git', 'remote', '-v'])
    return stdout


def add_remote_and_push(username: str, repo_name: str = "grass"):
    """원격 저장소 추가 및 푸시"""
    url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"🔗 원격 저장소 추가: {url}")
    success, stdout, stderr = run_command(['git', 'remote', 'add', 'origin', url])
    
    if not success:
        # 이미 존재하는 경우
        if 'already exists' in stderr.lower():
            print("ℹ️  원격 저장소가 이미 설정되어 있습니다.")
            # 기존 원격 저장소 제거 후 다시 추가
            run_command(['git', 'remote', 'remove', 'origin'])
            run_command(['git', 'remote', 'add', 'origin', url])
        else:
            print(f"❌ 실패: {stderr}")
            return False
    
    print("✅ 원격 저장소 추가 완료!")
    print()
    
    # 푸시
    print("🚀 GitHub에 푸시 중...")
    success, stdout, stderr = run_command(['git', 'push', '-u', 'origin', 'master'])
    
    if success:
        print("✅ 푸시 완료!")
        print(f"\n📦 GitHub 저장소: https://github.com/{username}/{repo_name}")
        return True
    else:
        print(f"❌ 푸시 실패: {stderr}")
        print("\n가능한 원인:")
        print("1. GitHub 저장소가 존재하지 않음")
        print("2. 인증 문제 (Personal Access Token 필요)")
        print("3. 저장소 이름이 다름")
        return False


def main():
    """메인 함수"""
    print("=" * 60)
    print("로컬 커밋을 GitHub로 전송")
    print("=" * 60)
    print()
    
    # 현재 커밋 확인
    success, stdout, _ = run_command(['git', 'log', '--oneline', '-1'])
    if success and stdout:
        print(f"📝 최신 커밋: {stdout}")
    print()
    
    # 원격 저장소 확인
    remote = check_remote()
    if remote:
        print("✅ 원격 저장소가 이미 설정되어 있습니다:")
        print(remote)
        print()
        print("🚀 바로 푸시하시겠습니까? (y/n): ", end='')
        # choice = input().strip().lower()
        # if choice == 'y':
        #     success, stdout, stderr = run_command(['git', 'push', '-u', 'origin', 'master'])
        #     if success:
        #         print("✅ 푸시 완료!")
        #     else:
        #         print(f"❌ 푸시 실패: {stderr}")
        return
    
    print("❌ 원격 저장소가 설정되어 있지 않습니다.")
    print()
    print("GitHub 사용자명을 입력하세요:")
    print("예: octocat")
    print()
    print("사용자명: ", end='')
    # username = input().strip()
    username = ""
    
    if not username:
        print("\n⚠️  GitHub 사용자명이 필요합니다.")
        print("\n다음 중 하나를 선택하세요:")
        print()
        print("방법 1: Cursor UI 사용 (가장 쉬움)")
        print("  1. Ctrl + Shift + G (소스 제어)")
        print("  2. '...' 메뉴 클릭")
        print("  3. 'Publish to GitHub' 선택")
        print("  4. 저장소 이름 입력 후 생성")
        print()
        print("방법 2: GitHub에서 저장소 생성 후")
        print("  - https://github.com/new 접속")
        print("  - 저장소 생성")
        print("  - 사용자명을 알려주시면 연결하겠습니다")
        return
    
    repo_name = "grass"
    print(f"\n저장소 이름 (기본: {repo_name}): ", end='')
    # repo_input = input().strip()
    # if repo_input:
    #     repo_name = repo_input
    
    add_remote_and_push(username, repo_name)


if __name__ == '__main__':
    main()

