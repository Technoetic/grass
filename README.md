# 코드 실행 시 자동 커밋

코드를 실행하면 자동으로 Git 커밋이 수행됩니다.

## 사용 방법

### 방법 1: run.py 사용 (추천)

```bash
python run.py 251220.py
```

### 방법 2: run.bat 사용 (Windows)

```bash
run.bat 251220.py
```

### 방법 3: 직접 사용

```bash
python auto_commit_on_run.py 251220.py
```

## 작동 방식

1. 스크립트 실행
2. 실행 완료 후 Git 상태 확인
3. 변경사항이 있으면 자동 커밋
4. 커밋 메시지 자동 생성

## 예제

```bash
# 기본 실행
python run.py 251220.py

# 인자 전달
python run.py script.py arg1 arg2
```

## 설정

```bash
python setup_auto_commit.py
```

---

이제 코드를 실행하면 자동으로 커밋됩니다! 🚀

