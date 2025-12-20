"""
실시간 동기화 시작 스크립트
간단하게 실행할 수 있는 래퍼 스크립트
"""
import sys
from sync_watcher import SyncWatcher

if __name__ == '__main__':
    print("🚀 실시간 동기화를 시작합니다...\n")
    
    try:
        watcher = SyncWatcher(auto_push=True, debounce=5)
        watcher.start()
    except KeyboardInterrupt:
        print("\n\n👋 동기화를 종료합니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)

