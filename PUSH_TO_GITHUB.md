# GitHub에 푸시하기

로컬 커밋이 완료되었습니다! 이제 GitHub에 푸시하려면 다음 단계를 따르세요.

## 방법 1: 기존 GitHub 저장소에 푸시

GitHub에 이미 저장소가 있다면:

```bash
# 원격 저장소 추가
git remote add origin https://github.com/your-username/your-repo.git

# 푸시
git push -u origin master
```

## 방법 2: 새 GitHub 저장소 만들기

1. **GitHub에서 새 저장소 생성**
   - https://github.com/new 접속
   - 저장소 이름 입력 (예: `grass`)
   - Public 또는 Private 선택
   - "Initialize this repository with a README" 체크 해제 (이미 파일이 있으므로)
   - "Create repository" 클릭

2. **원격 저장소 연결 및 푸시**
   ```bash
   # 원격 저장소 추가 (GitHub에서 제공하는 URL 사용)
   git remote add origin https://github.com/your-username/grass.git
   
   # 푸시
   git push -u origin master
   ```

## 방법 3: 스크립트 사용

아래 명령어로 원격 저장소를 설정할 수 있습니다:

```bash
# 원격 저장소 추가
git remote add origin YOUR_GITHUB_REPO_URL

# 푸시
git push -u origin master
```

## 인증 방법

### Personal Access Token 사용 (권장)

1. GitHub에서 토큰 생성:
   - https://github.com/settings/tokens
   - "Generate new token (classic)"
   - `repo` 권한 선택
   - 토큰 생성 후 복사

2. 푸시 시 사용자명과 토큰 입력:
   ```
   Username: your-username
   Password: your-personal-access-token
   ```

### SSH 키 사용

1. SSH 키 생성:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 공개 키를 GitHub에 추가:
   - https://github.com/settings/keys
   - "New SSH key" 클릭
   - 공개 키 내용 붙여넣기

3. SSH URL로 원격 저장소 설정:
   ```bash
   git remote add origin git@github.com:your-username/grass.git
   git push -u origin master
   ```

## 문제 해결

### "remote origin already exists" 오류
```bash
# 기존 원격 저장소 제거 후 다시 추가
git remote remove origin
git remote add origin YOUR_GITHUB_REPO_URL
```

### "Authentication failed" 오류
- Personal Access Token을 사용하세요 (비밀번호가 아닙니다)
- 토큰에 `repo` 권한이 있는지 확인하세요

### "branch 'master' has no upstream branch" 오류
```bash
git push -u origin master
```
`-u` 옵션으로 업스트림 브랜치를 설정하세요.


