# GitHub Grass (잔디) 연동 프로젝트

Cursor IDE에서 GitHub 잔디(contribution graph)를 관리하기 위한 도구 모음입니다.

## 기능

### 1. GitHub API 연동
- ✅ GitHub API 인증 (Personal Access Token)
- ✅ 사용자 정보 조회
- ✅ 저장소 목록 및 통계 조회
- ✅ Contribution 관련 데이터 수집

### 2. Git 자동 커밋 (Cursor 통합)
- ✅ Cursor IDE의 Git 통합 활용
- ✅ 변경사항 자동 감지 및 커밋
- ✅ 간편한 커밋 명령어 제공
- ✅ 커밋 로그 조회

### 3. 실시간 자동 커밋 ⭐ NEW!
- ✅ 파일 변경 시 자동 커밋
- ✅ 스마트 디바운스 (여러 변경사항 묶기)
- ✅ 자동 커밋 메시지 생성
- ✅ 불필요한 파일 자동 제외

## 설치

1. Python 3.7 이상이 필요합니다.

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. Git 저장소 초기화 (선택사항):
```bash
python setup_git.py
```
또는 직접:
```bash
git init
```

## 설정

1. `env.example` 파일을 `.env`로 복사:
```bash
copy env.example .env
```

2. GitHub Personal Access Token 생성:
   - https://github.com/settings/tokens 접속
   - "Generate new token" 클릭
   - 필요한 권한 선택 (최소: `public_repo`)
   - 토큰 생성 후 복사

3. `.env` 파일에 토큰 추가:
```
GITHUB_TOKEN=your_github_token_here
```

## 사용법

### 기본 사용

```python
from github_api import GitHubAPI

# API 클라이언트 생성 (환경변수에서 토큰 자동 로드)
api = GitHubAPI()

# 또는 직접 토큰 지정
api = GitHubAPI(token='your_token_here')

# 사용자 정보 가져오기
user_info = api.get_user_info()
print(user_info)

# 특정 사용자 정보 가져오기
user_info = api.get_user_info('octocat')

# 저장소 목록 가져오기
repos = api.get_user_repos()
print(repos)

# Contribution 정보 가져오기
contributions = api.get_contributions('username')
print(contributions)

# 최근 이벤트 가져오기
events = api.get_events('username')
print(events)
```

### Git 자동 커밋 (Cursor 통합)

#### 빠른 시작

1. **저장소 상태 확인:**
```bash
python commit_helper.py status
```

2. **변경사항 커밋:**
```bash
python commit_helper.py commit -m "업데이트 내용"
```

3. **커밋 및 푸시:**
```bash
python commit_helper.py commit -m "업데이트" --push
```

4. **커밋 로그 보기:**
```bash
python commit_helper.py log
```

#### Python 코드로 사용

```python
from git_auto_commit import GitAutoCommit

# Git 저장소 초기화
git = GitAutoCommit()

# 상태 확인
status = git.check_status()
print(f"변경사항: {status['count']}개 파일")

# 자동 커밋 (변경사항이 있을 때만)
result = git.auto_commit(message="업데이트", push=False)
if result['success']:
    print("✅ 커밋 성공!")
```

#### Cursor IDE에서 사용하기

1. **터미널 열기**: `Ctrl + `` (백틱) 또는 `View > Terminal`
2. **명령어 실행**: 위의 커밋 명령어 사용
3. **단축키 설정** (선택사항): Cursor 설정에서 키보드 단축키 추가

### 실시간 자동 커밋 (파일 변경 시 자동 커밋) ⭐

```bash
# 기본 실행 (파일 저장 시 자동 커밋)
python auto_commit_watcher.py

# 자동 푸시 포함
python auto_commit_watcher.py --push

# 디바운스 시간 조정 (30초)
python auto_commit_watcher.py --debounce 30

# 간단한 실행
python start_watcher.py
```

**작동 방식:**
1. 감시 시작
2. 파일을 수정하고 저장
3. 자동으로 커밋됨! (5초 디바운스)

자세한 내용은 `AUTO_COMMIT_GUIDE.md` 참고

### 테스트 실행

```bash
# GitHub API 테스트
python github_api.py

# Git 커밋 도구 테스트
python git_auto_commit.py

# 예제 실행
python example.py
```

## 주의사항

⚠️ **GitHub API 제한사항:**
- GitHub API는 직접적으로 contribution graph 데이터를 제공하지 않습니다.
- Contribution graph는 GitHub 웹사이트에서만 볼 수 있습니다.
- API를 통해 저장소 정보, 이벤트 등을 수집하여 간접적으로 활동을 파악할 수 있습니다.

⚠️ **자동 커밋 사용 시:**
- 이 도구는 **실제 파일 변경사항이 있을 때만** 커밋합니다.
- 빈 커밋이나 의미 없는 커밋은 생성하지 않습니다.
- 실제 프로젝트 활동을 기록하는 용도로 사용하세요.
- GitHub 서비스 약관을 준수하여 사용하세요.

## API 엔드포인트

- 사용자 정보: `/user` 또는 `/users/{username}`
- 저장소 목록: `/user/repos` 또는 `/users/{username}/repos`
- 이벤트: `/users/{username}/events/public`

## 라이선스

MIT

