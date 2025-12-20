"""
GitHub API 연동 사용 예제
"""
from github_api import GitHubAPI
import os
from dotenv import load_dotenv

load_dotenv()


def example_basic_usage():
    """기본 사용 예제"""
    print("=" * 50)
    print("기본 사용 예제")
    print("=" * 50)
    
    # API 클라이언트 생성
    api = GitHubAPI()
    
    # 인증 확인
    if not api.check_authentication():
        print("❌ 인증 실패")
        return
    
    # 사용자 정보
    user = api.get_user_info()
    print(f"\n👤 {user['login']} ({user.get('name', 'N/A')})")
    print(f"📊 Public Repos: {user['public_repos']}")
    print(f"👥 Followers: {user['followers']}")


def example_get_repos():
    """저장소 조회 예제"""
    print("\n" + "=" * 50)
    print("저장소 조회 예제")
    print("=" * 50)
    
    api = GitHubAPI()
    
    # 내 저장소 목록
    repos = api.get_user_repos(per_page=5)
    print(f"\n📦 최근 저장소 {len(repos)}개:")
    for repo in repos:
        print(f"  - {repo['name']} ({repo.get('language', 'N/A')})")


def example_get_contributions():
    """Contribution 정보 조회 예제"""
    print("\n" + "=" * 50)
    print("Contribution 정보 조회 예제")
    print("=" * 50)
    
    api = GitHubAPI()
    user = api.get_user_info()
    username = user['login']
    
    contributions = api.get_contributions(username)
    print(f"\n📊 Contribution 통계:")
    print(f"  - Public Repos: {contributions['public_repos']}")
    print(f"  - Total Repos: {contributions['total_repos']}")
    print(f"\n최근 활동 저장소:")
    for repo in contributions['repos'][:3]:
        print(f"  - {repo['full_name']} ⭐{repo['stars']}")


def example_get_events():
    """이벤트 조회 예제"""
    print("\n" + "=" * 50)
    print("이벤트 조회 예제")
    print("=" * 50)
    
    api = GitHubAPI()
    user = api.get_user_info()
    username = user['login']
    
    events = api.get_events(username, per_page=5)
    print(f"\n📅 최근 이벤트 {len(events)}개:")
    for event in events:
        event_type = event.get('type', 'N/A')
        repo = event.get('repo', {}).get('name', 'N/A')
        print(f"  - {event_type}: {repo}")


if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️  GITHUB_TOKEN 환경변수를 설정하세요.")
        print("   .env 파일을 생성하고 GITHUB_TOKEN=your_token 을 추가하세요.")
    else:
        example_basic_usage()
        example_get_repos()
        example_get_contributions()
        example_get_events()

