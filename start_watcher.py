"""
실시간 커밋 감시 시작 스크립트
간단하게 실행할 수 있는 래퍼 스크립트
"""
import sys
from auto_commit_watcher import AutoCommitWatcher

if __name__ == '__main__':
    print("🚀 실시간 자동 커밋 감시를 시작합니다...\n")
    
    try:
        watcher = AutoCommitWatcher()
        watcher.start()
    except KeyboardInterrupt:
        print("\n\n👋 감시를 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


