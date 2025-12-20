# 빠른 시작 가이드

Cursor IDE에서 GitHub 잔디를 관리하는 가장 빠른 방법입니다.

## 1단계: Git 저장소 초기화

현재 프로젝트가 Git 저장소가 아니라면:

```bash
python setup_git.py
```

또는 직접:
```bash
git init
```

## 2단계: GitHub 원격 저장소 연결 (선택사항)

```bash
git remote add origin https://github.com/your-username/your-repo.git
```

## 3단계: 파일 수정 및 커밋

### 방법 1: 커맨드라인 사용 (추천)

Cursor의 터미널(`Ctrl + ``)에서:

```bash
# 상태 확인
python commit_helper.py status

# 커밋
python commit_helper.py commit -m "업데이트"

# 커밋 + 푸시
python commit_helper.py commit -m "업데이트" --push
```

### 방법 2: Cursor의 Git UI 사용

1. 왼쪽 사이드바에서 소스 제어 아이콘 클릭 (또는 `Ctrl + Shift + G`)
2. 변경된 파일 확인
3. "+" 버튼으로 스테이징
4. 커밋 메시지 입력
5. "✓" 버튼으로 커밋
6. "..." 메뉴에서 "Push" 선택

## 4단계: 자동화 (선택사항)

정기적으로 커밋하려면 작업 스케줄러나 cron을 사용하세요.

### Windows 작업 스케줄러 예제:

```powershell
# 매일 오후 6시에 실행
schtasks /create /tn "GitAutoCommit" /tr "python D:\Project\grass\commit_helper.py commit -m 'Daily update'" /sc daily /st 18:00
```

## 팁

- **의미 있는 커밋**: 실제로 변경사항이 있을 때만 커밋하세요
- **규칙적인 활동**: 매일 조금씩 작업하는 것이 좋습니다
- **커밋 메시지**: 무엇을 했는지 명확하게 작성하세요

## 문제 해결

### "Git 저장소가 아닙니다" 오류
→ `python setup_git.py` 실행

### "커밋할 변경사항이 없습니다"
→ 파일을 수정하거나 새 파일을 추가하세요

### 푸시 실패
→ GitHub 인증 확인 및 원격 저장소 URL 확인


