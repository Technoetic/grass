# Cursor IDE GitHub 통합 가이드

Cursor IDE가 GitHub 계정으로 로그인되어 있다면, 이를 활용하여 쉽게 저장소를 설정할 수 있습니다.

## 현재 상태

✅ **Cursor IDE**: GitHub 계정 로그인됨  
❌ **Git 원격 저장소**: 아직 설정 안 됨

## Cursor의 GitHub 통합 활용하기

### 방법 1: Cursor UI로 직접 퍼블리시 (가장 쉬움) ⭐

1. **소스 제어 패널 열기**
   - `Ctrl + Shift + G` 또는
   - 왼쪽 사이드바의 소스 제어 아이콘 클릭

2. **GitHub에 퍼블리시**
   - 상단의 "..." 메뉴 클릭
   - **"Publish to GitHub"** 선택
   - 저장소 이름 입력 (예: `grass`)
   - Public 또는 Private 선택
   - **"Publish"** 클릭

3. **완료!**
   - Cursor가 자동으로:
     - GitHub에 새 저장소 생성
     - 원격 저장소 연결
     - 첫 커밋 푸시

### 방법 2: 수동으로 원격 저장소 추가

Cursor의 GitHub 로그인 정보를 활용하여 수동으로 설정:

1. **GitHub에서 저장소 생성**
   - https://github.com/new 접속
   - 저장소 이름: `grass`
   - Public/Private 선택
   - "Create repository" 클릭

2. **원격 저장소 연결**
   ```bash
   git remote add origin https://github.com/your-username/grass.git
   git push -u origin master
   ```

   Cursor가 GitHub에 로그인되어 있으면 인증이 자동으로 처리될 수 있습니다.

### 방법 3: GitHub CLI 사용 (선택사항)

GitHub CLI가 설치되어 있다면:

```bash
# GitHub CLI로 로그인 확인
gh auth status

# 저장소 생성 및 연결
gh repo create grass --public --source=. --remote=origin --push
```

## 확인 방법

### 원격 저장소 확인

```bash
git remote -v
```

출력 예시:
```
origin  https://github.com/your-username/grass.git (fetch)
origin  https://github.com/your-username/grass.git (push)
```

### 푸시 테스트

```bash
git push -u origin master
```

## Cursor의 GitHub 통합 기능

Cursor IDE가 GitHub에 로그인되어 있으면:

- ✅ **자동 인증**: Git 명령어 실행 시 자동으로 인증
- ✅ **원클릭 퍼블리시**: UI에서 바로 GitHub에 퍼블리시
- ✅ **설정 동기화**: Cursor 설정이 GitHub와 동기화
- ✅ **코드 공유**: Cursor의 협업 기능 사용 가능

## 문제 해결

### "Publish to GitHub" 옵션이 보이지 않음

- Cursor가 GitHub에 로그인되어 있는지 확인
- `Ctrl + Shift + P` → "GitHub: Sign in" 실행

### 푸시 시 인증 오류

1. **Personal Access Token 사용**
   - https://github.com/settings/tokens
   - 토큰 생성 (repo 권한)
   - Git Credential Manager에 저장

2. **SSH 키 사용**
   - SSH 키 생성 및 GitHub에 추가
   - SSH URL로 원격 저장소 설정

### Cursor에서 GitHub 로그인 확인

- `Ctrl + Shift + P` → "GitHub: Show Account" 실행
- 또는 설정에서 GitHub 계정 확인

## 다음 단계

원격 저장소가 설정되면:

1. **로컬 커밋 푸시**
   ```bash
   git push -u origin master
   ```

2. **실시간 자동 커밋 + 푸시**
   ```bash
   python auto_commit_watcher.py --push
   ```

3. **GitHub에서 확인**
   - https://github.com/your-username/grass 접속
   - 파일들이 업로드되어 있는지 확인

---

**추천**: Cursor의 "Publish to GitHub" 기능을 사용하면 가장 쉽고 빠릅니다! 🚀


