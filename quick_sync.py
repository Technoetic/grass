"""
빠른 실시간 동기화 시작
백그라운드에서 실행되도록 개선
"""
import subprocess
import sys
import os
from pathlib import Path

def start_background_sync():
    """백그라운드에서 실시간 동기화 시작"""
    script_path = Path(__file__).parent / 'sync_watcher.py'
    
    if os.name == 'nt':  # Windows
        # PowerShell로 백그라운드 실행
        ps_script = f'''
$job = Start-Job -ScriptBlock {{
    cd "{Path.cwd()}"
    python "{script_path}"
}}
Write-Host "✅ 실시간 동기화가 백그라운드에서 시작되었습니다."
Write-Host "   작업 ID: $job.Id"
Write-Host "   중지하려면: Stop-Job -Id $job.Id"
Receive-Job -Job $job -Wait
'''
        subprocess.run(['powershell', '-Command', ps_script])
    else:  # Linux/Mac
        subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ 실시간 동기화가 백그라운드에서 시작되었습니다.")

if __name__ == '__main__':
    print("=" * 60)
    print("실시간 동기화 시작")
    print("=" * 60)
    print()
    print("선택:")
    print("1. 포그라운드 실행 (콘솔에서 확인 가능)")
    print("2. 백그라운드 실행 (백그라운드에서 실행)")
    print()
    print("기본: 포그라운드 실행")
    print()
    
    # 기본적으로 포그라운드 실행
    from sync_watcher import SyncWatcher
    watcher = SyncWatcher(auto_push=True, debounce=5)
    watcher.start()

