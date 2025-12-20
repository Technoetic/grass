# GitHub 사용자명 확인 방법

GitHub 사용자명을 확인하는 여러 방법입니다.

## 방법 1: Cursor IDE에서 확인 (가장 쉬움) ⭐

1. **명령 팔레트 열기**
   - `Ctrl + Shift + P`

2. **GitHub 계정 확인**
   - "GitHub: Show Account" 입력
   - 또는 "GitHub: Sign in" 입력하여 로그인 상태 확인

3. **소스 제어 패널에서 확인**
   - `Ctrl + Shift + G` (소스 제어 열기)
   - "..." 메뉴 클릭
   - "Publish to GitHub" 선택 시 사용자명이 표시될 수 있음

## 방법 2: GitHub 웹사이트에서 확인

1. **GitHub.com 접속**
   - https://github.com

2. **프로필 확인**
   - 우측 상단 프로필 사진 클릭
   - 사용자명 확인 (프로필 URL에 표시됨)
   - 예: `https://github.com/your-username`

## 방법 3: 브라우저에서 확인

GitHub에 로그인되어 있다면:
- 주소창에 `github.com` 입력
- 자동완성에서 사용자명 확인
- 또는 우측 상단 프로필에서 확인

## 방법 4: 이메일로 확인

GitHub 계정 이메일을 알고 있다면:
- Git 설정 확인: `git config user.email`
- GitHub에서 이메일로 사용자 찾기

## 사용자명을 알았으면

사용자명을 알려주시면 바로 원격 저장소를 연결하겠습니다:

```bash
git remote add origin https://github.com/your-username/grass.git
git push -u origin master
```

---

**또는** Cursor의 "Publish to GitHub" 기능을 사용하면 사용자명을 입력할 필요가 없습니다!


