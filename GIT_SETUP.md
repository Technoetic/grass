# Git 설치 가이드

Git이 설치되어 있지 않아서 커밋을 진행할 수 없습니다. 다음 방법으로 Git을 설치하세요.

## Windows에서 Git 설치하기

### 방법 1: 공식 웹사이트에서 다운로드 (추천)

1. **Git 공식 웹사이트 방문**
   - https://git-scm.com/download/win

2. **다운로드 및 설치**
   - 자동으로 다운로드가 시작됩니다
   - 설치 프로그램 실행
   - 기본 설정으로 "Next" 클릭 (권장)
   - 설치 완료 후 컴퓨터 재시작

3. **설치 확인**
   ```powershell
   git --version
   ```

### 방법 2: 패키지 매니저 사용

#### Chocolatey 사용
```powershell
choco install git
```

#### Winget 사용
```powershell
winget install --id Git.Git -e --source winget
```

#### Scoop 사용
```powershell
scoop install git
```

## 설치 후 확인

터미널을 다시 열고 다음 명령어로 확인:

```powershell
git --version
```

출력 예시: `git version 2.xx.x`

## Git 설정 (처음 한 번만)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 설치 후 다시 시도

Git 설치가 완료되면:

1. **Cursor 터미널을 다시 열기** (중요!)

2. **Git 저장소 초기화**
   ```bash
   python setup_git.py
   ```

3. **커밋**
   ```bash
   python commit_helper.py commit -m "초기 커밋"
   ```

---

## Git 없이 GitHub에 업로드하는 방법

Git이 설치되어 있지 않다면, GitHub 웹사이트에서 직접 업로드할 수도 있습니다:

1. GitHub.com에 로그인
2. 새 저장소 생성 (New repository)
3. "uploading an existing file" 클릭
4. 파일들을 드래그 앤 드롭
5. 커밋 메시지 입력 후 "Commit changes"

---

## 문제 해결

### "git is not recognized" 오류
- Git 설치 후 **터미널을 다시 시작**하세요
- 또는 컴퓨터를 재시작하세요

### PATH 문제
- Git 설치 시 "Add Git to PATH" 옵션을 선택했는지 확인
- 설치 프로그램을 다시 실행하여 PATH 추가


