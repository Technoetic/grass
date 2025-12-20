# 코드 실행 시 자동 커밋 & 실시간 동기화

코드를 실행하면 자동으로 커밋되고, 파일 변경 시 실시간으로 GitHub와 동기화됩니다.

## 기능

### 1. 코드 실행 시 자동 커밋

```bash
python run.py 251220.py
```

코드를 실행하면 자동으로 Git 커밋이 수행됩니다.

### 2. 실시간 동기화 (파일 변경 시 자동 커밋 + 푸시) ⭐

```bash
python start_sync.py
```

파일을 수정하고 저장하면 자동으로:
- 커밋
- GitHub에 푸시

## 사용 방법

### 코드 실행 시 자동 커밋

```bash
# 방법 1: run.py 사용
python run.py 251220.py

# 방법 2: run.bat 사용 (Windows)
run.bat 251220.py

# 방법 3: 직접 사용
python auto_commit_on_run.py 251220.py
```

### 실시간 동기화

```bash
# 기본 실행 (자동 푸시 포함)
python start_sync.py

# 또는 직접 실행
python sync_watcher.py

# 옵션 사용
python sync_watcher.py --debounce 10    # 디바운스 10초
python sync_watcher.py --no-push        # 푸시 없이 커밋만
```

## 작동 방식

### 코드 실행 시
1. 스크립트 실행
2. 실행 완료 후 Git 상태 확인
3. 변경사항이 있으면 자동 커밋

### 실시간 동기화
1. 파일 변경 감지
2. 5초 디바운스 (여러 변경사항 묶기)
3. 자동 커밋
4. 자동 푸시 (GitHub와 동기화)

---

이제 파일을 수정하면 자동으로 GitHub와 동기화됩니다! 🚀
