"""
GitHub API 연동 모듈
GitHub 잔디(contribution graph) 및 사용자 정보를 가져오는 기능 제공
"""
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class GitHubAPI:
    """GitHub API 클라이언트"""
    
    def __init__(self, token: Optional[str] = None):
        """
        GitHub API 클라이언트 초기화
        
        Args:
            token: GitHub Personal Access Token (없으면 환경변수에서 가져옴)
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}' if self.token else None
        }
        # Authorization 헤더가 None이면 제거
        if not self.headers['Authorization']:
            self.headers.pop('Authorization')
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        GitHub API 요청
        
        Args:
            endpoint: API 엔드포인트 (예: '/user')
            params: 쿼리 파라미터
            
        Returns:
            API 응답 데이터
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, username: Optional[str] = None) -> Dict:
        """
        사용자 정보 가져오기
        
        Args:
            username: GitHub 사용자명 (없으면 인증된 사용자)
            
        Returns:
            사용자 정보 딕셔너리
        """
        endpoint = f'/users/{username}' if username else '/user'
        return self._request(endpoint)
    
    def get_user_repos(self, username: Optional[str] = None, 
                      per_page: int = 100) -> List[Dict]:
        """
        사용자의 저장소 목록 가져오기
        
        Args:
            username: GitHub 사용자명 (없으면 인증된 사용자)
            per_page: 페이지당 항목 수
            
        Returns:
            저장소 목록
        """
        endpoint = f'/users/{username}/repos' if username else '/user/repos'
        repos = []
        page = 1
        
        while True:
            params = {'per_page': per_page, 'page': page, 'sort': 'updated'}
            response = self._request(endpoint, params)
            if not response:
                break
            repos.extend(response)
            if len(response) < per_page:
                break
            page += 1
        
        return repos
    
    def get_contributions(self, username: str) -> Dict:
        """
        사용자의 contribution 통계 가져오기
        (참고: GitHub API는 직접적으로 contribution graph를 제공하지 않음)
        
        Args:
            username: GitHub 사용자명
            
        Returns:
            Contribution 관련 통계
        """
        user_info = self.get_user_info(username)
        repos = self.get_user_repos(username)
        
        # 저장소별 contribution 정보 수집
        contributions = {
            'public_repos': user_info.get('public_repos', 0),
            'total_repos': len(repos),
            'repos': []
        }
        
        for repo in repos[:10]:  # 최근 10개만
            repo_info = {
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'updated_at': repo.get('updated_at'),
                'language': repo.get('language')
            }
            contributions['repos'].append(repo_info)
        
        return contributions
    
    def get_events(self, username: str, per_page: int = 30) -> List[Dict]:
        """
        사용자의 최근 이벤트 가져오기
        
        Args:
            username: GitHub 사용자명
            per_page: 페이지당 항목 수
            
        Returns:
            이벤트 목록
        """
        endpoint = f'/users/{username}/events/public'
        params = {'per_page': per_page}
        return self._request(endpoint, params)
    
    def check_authentication(self) -> bool:
        """
        인증 상태 확인
        
        Returns:
            인증 성공 여부
        """
        try:
            self._request('/user')
            return True
        except:
            return False


def main():
    """테스트 함수"""
    print("GitHub API 연동 테스트\n")
    
    # 환경변수에서 토큰 확인
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️  GITHUB_TOKEN 환경변수가 설정되지 않았습니다.")
        print("   .env 파일에 GITHUB_TOKEN=your_token 을 추가하세요.")
        print("\n   또는 GitHub에서 Personal Access Token을 생성하세요:")
        print("   https://github.com/settings/tokens")
        return
    
    # API 클라이언트 생성
    api = GitHubAPI(token)
    
    # 인증 확인
    if not api.check_authentication():
        print("❌ 인증 실패: 토큰이 유효하지 않습니다.")
        return
    
    print("✅ 인증 성공!\n")
    
    # 사용자 정보 가져오기
    user_info = api.get_user_info()
    print(f"👤 사용자: {user_info.get('login')}")
    print(f"📝 이름: {user_info.get('name', 'N/A')}")
    print(f"📧 이메일: {user_info.get('email', 'N/A')}")
    print(f"📊 Public Repos: {user_info.get('public_repos', 0)}")
    print(f"👥 Followers: {user_info.get('followers', 0)}")
    print(f"⭐ Following: {user_info.get('following', 0)}\n")
    
    # Contribution 정보
    username = user_info.get('login')
    contributions = api.get_contributions(username)
    print(f"📦 총 저장소 수: {contributions['total_repos']}")
    print(f"\n최근 활동 저장소:")
    for repo in contributions['repos'][:5]:
        print(f"  - {repo['full_name']} ({repo['language'] or 'N/A'}) ⭐{repo['stars']}")


if __name__ == '__main__':
    main()

