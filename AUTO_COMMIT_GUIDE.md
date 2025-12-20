# 실시간 자동 커밋 가이드

파일이 변경될 때마다 자동으로 Git 커밋을 수행하는 실시간 감시 도구입니다.

## 빠른 시작

### 기본 사용법

```bash
python auto_commit_watcher.py
```

또는 간단한 스크립트 사용:

```bash
python start_watcher.py
```

### 자동 푸시 포함

```bash
python auto_commit_watcher.py --push
```

## 기능

- ✅ **실시간 파일 변경 감지**: 파일이 저장되면 자동 감지
- ✅ **스마트 디바운스**: 여러 변경사항을 묶어서 한 번에 커밋 (기본 5초)
- ✅ **자동 커밋 메시지**: 변경된 파일명을 포함한 메시지 자동 생성
- ✅ **무시 패턴**: 불필요한 파일 자동 제외 (.pyc, .log 등)
- ✅ **안전한 커밋**: 실제 변경사항이 있을 때만 커밋

## 사용 방법

### 1. 기본 실행

```bash
python auto_commit_watcher.py
```

- 파일을 수정하고 저장하면 자동으로 커밋됩니다
- 중지하려면 `Ctrl+C`를 누르세요

### 2. 옵션 사용

```bash
# 자동 푸시 활성화
python auto_commit_watcher.py --push

# 디바운스 시간 조정 (10초)
python auto_commit_watcher.py --debounce 10

# 고정 커밋 메시지 사용
python auto_commit_watcher.py --no-auto-message --message "업데이트"

# 특정 디렉토리 감시
python auto_commit_watcher.py --path /path/to/repo
```

### 3. 설정 파일 사용

`config.json` 파일에서 설정:

```json
{
  "watcher": {
    "auto_message": true,
    "auto_push": false,
    "debounce_seconds": 5,
    "ignore_patterns": [".pyc", ".log"],
    "ignore_dirs": [".git", "__pycache__", "venv"]
  }
}
```

## 작동 방식

1. **파일 변경 감지**: 파일이 저장되면 감지
2. **디바운스 대기**: 5초 동안 추가 변경사항 대기
3. **변경사항 확인**: Git 상태 확인
4. **자동 커밋**: 변경사항이 있으면 자동 커밋
5. **푸시 (선택)**: 설정에 따라 자동 푸시

## 예시

### 시나리오 1: 일반적인 개발

```bash
# 감시 시작
python auto_commit_watcher.py

# 다른 터미널이나 Cursor에서 파일 수정
# README.md 저장 → 자동 커밋
# github_api.py 저장 → 자동 커밋
```

출력 예시:
```
✅ [14:30:15] 자동 커밋 완료: 자동 커밋: README.md (2025-12-20 14:30:15)
✅ [14:30:45] 자동 커밋 완료: 자동 커밋: github_api.py (2025-12-20 14:30:45)
```

### 시나리오 2: 자동 푸시

```bash
python auto_commit_watcher.py --push
```

파일 변경 시 자동으로 커밋 + 푸시

### 시나리오 3: 긴 디바운스

```bash
python auto_commit_watcher.py --debounce 30
```

30초 동안 여러 변경사항을 모아서 한 번에 커밋

## 무시되는 파일/디렉토리

기본적으로 다음은 자동으로 무시됩니다:

- `.git/` - Git 메타데이터
- `__pycache__/` - Python 캐시
- `venv/`, `env/`, `.venv/` - 가상환경
- `node_modules/` - Node.js 모듈
- `*.pyc`, `*.pyo`, `*.pyd` - Python 컴파일 파일
- `*.log`, `*.tmp` - 임시 파일

## 주의사항

⚠️ **실제 작업만 커밋**: 이 도구는 실제 파일 변경사항이 있을 때만 커밋합니다.

⚠️ **의미 있는 커밋**: 너무 자주 커밋하면 히스토리가 복잡해질 수 있습니다. 필요시 디바운스 시간을 늘리세요.

⚠️ **자동 푸시 주의**: `--push` 옵션 사용 시 자동으로 GitHub에 푸시됩니다. 신중하게 사용하세요.

## 문제 해결

### "watchdog 모듈을 찾을 수 없습니다"
```bash
pip install watchdog
```

### "커밋할 변경사항이 없습니다" 메시지가 계속 나옴
- 파일이 실제로 저장되었는지 확인
- `.gitignore`에 포함되어 있지 않은지 확인

### 너무 자주 커밋됨
- `--debounce` 시간을 늘리세요 (예: `--debounce 30`)

### 특정 파일이 감지되지 않음
- `config.json`의 `ignore_patterns` 확인
- 파일이 `.gitignore`에 포함되어 있지 않은지 확인

## 고급 사용법

### 백그라운드 실행 (Windows)

```powershell
Start-Process python -ArgumentList "auto_commit_watcher.py" -WindowStyle Hidden
```

### 로그 파일로 출력 저장

```bash
python auto_commit_watcher.py > watcher.log 2>&1
```

### 특정 파일만 감시

`config.json`에서 `ignore_patterns`를 조정하여 특정 파일만 커밋

---

이제 파일을 수정하고 저장하기만 하면 자동으로 커밋됩니다! 🎉


