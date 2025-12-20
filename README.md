# GitHub Grass (잔디) 프로젝트

코드 실행 시 자동 커밋 기능이 포함된 프로젝트입니다.

## 자동 커밋 기능

코드를 실행하면 자동으로 Git 커밋이 수행됩니다.

### 사용 방법

#### 방법 1: run.py 사용 (추천)

```bash
python run.py 251220.py
```

#### 방법 2: run.bat 사용 (Windows)

```bash
run.bat 251220.py
```

#### 방법 3: 직접 사용

```bash
python auto_commit_on_run.py 251220.py
```

## 작동 방식

1. 스크립트 실행
2. 실행 완료 후 Git 상태 확인
3. 변경사항이 있으면 자동 커밋
4. 커밋 메시지 자동 생성 (예: "자동 커밋: 251220.py 실행 (2025-12-20 23:37:02)")

## 예제

```bash
# 기본 실행
python run.py 251220.py

# 인자 전달
python run.py script.py arg1 arg2
```

## GitHub 푸시

커밋 후 GitHub에 푸시:

```bash
git push
```

---

이제 코드를 실행하면 자동으로 커밋됩니다! 🚀
