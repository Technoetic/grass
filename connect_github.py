"""
GitHub 원격 저장소 연결 도우미
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


def add_remote(url: str):
    """원격 저장소 추가"""
    # 기존 원격 저장소 확인
    current_remotes = check_remote()
    if current_remotes:
        print("⚠️  이미 원격 저장소가 설정되어 있습니다:")
        print(current_remotes)
        print("\n덮어쓰시겠습니까? (y/n): ", end='')
        # choice = input().strip().lower()
        # if choice != 'y':
        #     return False
        # 기존 원격 저장소 제거
        run_command(['git', 'remote', 'remove', 'origin'])
    
    # 새 원격 저장소 추가
    success, stdout, stderr = run_command(['git', 'remote', 'add', 'origin', url])
    if success:
        print(f"✅ 원격 저장소 추가 완료: {url}")
        return True
    else:
        print(f"❌ 실패: {stderr}")
        return False


def test_connection():
    """연결 테스트"""
    print("\n🔍 원격 저장소 연결 테스트 중...")
    success, stdout, stderr = run_command(['git', 'remote', 'show', 'origin'])
    if success:
        print("✅ 연결 성공!")
        print(stdout)
        return True
    else:
        print(f"⚠️  연결 확인 실패: {stderr}")
        print("   저장소가 비공개이거나 인증이 필요할 수 있습니다.")
        return False


def main():
    """메인 함수"""
    print("=" * 60)
    print("GitHub 원격 저장소 연결 도우미")
    print("=" * 60)
    print()
    
    # 현재 원격 저장소 확인
    remotes = check_remote()
    if remotes:
        print("현재 원격 저장소:")
        print(remotes)
        print()
    else:
        print("❌ 원격 저장소가 설정되어 있지 않습니다.")
        print()
    
    print("GitHub 저장소 URL을 입력하세요:")
    print("예: https://github.com/username/grass.git")
    print("또는: git@github.com:username/grass.git")
    print()
    print("URL: ", end='')
    
    # 실제 사용 시에는 input() 사용
    # url = input().strip()
    url = ""  # 여기에 URL 입력
    
    if not url:
        print("\n⚠️  URL이 입력되지 않았습니다.")
        print("\n수동으로 연결하는 방법:")
        print("  git remote add origin https://github.com/your-username/your-repo.git")
        print("  git push -u origin master")
        return
    
    if add_remote(url):
        test_connection()
        print("\n✅ 설정 완료!")
        print("\n다음 단계:")
        print("  git push -u origin master")


if __name__ == '__main__':
    main()


