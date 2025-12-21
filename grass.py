import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 메인 로직 실행
n = int(input())
result = sum(range(1, n+1))
print(result)

# 실행 후 자동으로 git push 수행
try:
    # Git 상태 확인
    status_result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if status_result.stdout.strip():
        # 변경사항이 있으면 커밋
        subprocess.run(
            ['git', 'add', '.'],
            check=True,
            capture_output=True
        )
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"자동 커밋: grass.py 실행 ({timestamp})"
        
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if commit_result.returncode == 0:
            # 푸시 수행
            push_result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if push_result.returncode == 0:
                # 브랜치 정보 가져오기
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                branch_name = branch_result.stdout.strip() if branch_result.returncode == 0 else '알 수 없음'
                
                # 원격 저장소 정보 가져오기
                remote_result = subprocess.run(
                    ['git', 'remote', 'get-url', 'origin'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else '알 수 없음'
                
                # 최근 커밋 해시 가져오기
                commit_hash_result = subprocess.run(
                    ['git', 'log', '-1', '--format=%h'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                commit_hash = commit_hash_result.stdout.strip() if commit_hash_result.returncode == 0 else ''
                
                # 상세한 푸시 확인 메시지 출력
                print()
                print("=" * 60)
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Git Push 완료!")
                print("=" * 60)
                print(f"📦 브랜치: {branch_name}")
                print(f"🔗 원격 저장소: {remote_url}")
                if commit_hash:
                    print(f"📝 커밋 해시: {commit_hash}")
                print(f"⏰ 푸시 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 60)
            else:
                print(f"⚠️  푸시 실패: {push_result.stderr}")
        else:
            print(f"⚠️  커밋 실패: {commit_result.stderr}")
    else:
        # 변경사항이 없어도 이미 푸시된 상태인지 확인하고 메시지 출력
        print()
        print("=" * 60)
        print(f"ℹ️  [{datetime.now().strftime('%H:%M:%S')}] 커밋할 변경사항이 없습니다.")
        print("=" * 60)
        
except Exception as e:
    # Git 오류가 발생해도 메인 로직은 정상 실행됨
    pass