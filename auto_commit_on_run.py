"""
코드 실행 시 자동 커밋 도구
Python 스크립트를 실행하면 자동으로 Git 커밋을 수행합니다.
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def run_and_commit(script_path: str, *args):
    """
    스크립트를 실행하고 자동으로 커밋
    
    Args:
        script_path: 실행할 Python 스크립트 경로
        *args: 스크립트에 전달할 인자들
    """
    script_path = Path(script_path)
    
    if not script_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {script_path}")
        return False
    
    print("=" * 60)
    print("코드 실행 및 자동 커밋")
    print("=" * 60)
    print()
    
    # 1. 스크립트 실행
    print(f"🚀 스크립트 실행 중: {script_path.name}")
    print()
    
    try:
        cmd = [sys.executable, str(script_path)] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True
        )
        
        exit_code = result.returncode
        print()
        
        if exit_code != 0:
            print(f"⚠️  스크립트 실행 실패 (종료 코드: {exit_code})")
            print("   실행은 완료되었지만, 커밋은 수행하지 않습니다.")
            # 실행 실패해도 변경사항이 있으면 커밋할 수 있도록 옵션 제공
            return False
        
        print("✅ 스크립트 실행 완료!")
        print()
        
    except Exception as e:
        print(f"❌ 실행 오류: {e}")
        return False
    
    # 2. Git 상태 확인
    print("📊 Git 상태 확인 중...")
    try:
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if not status_result.stdout.strip():
            print("ℹ️  커밋할 변경사항이 없습니다.")
            return True
        
        changed_files = [line for line in status_result.stdout.strip().split('\n') if line.strip()]
        print(f"📝 변경된 파일: {len(changed_files)}개")
        
    except Exception as e:
        print(f"⚠️  Git 상태 확인 실패: {e}")
        return False
    
    # 3. 자동 커밋
    print()
    print("💾 자동 커밋 수행 중...")
    
    try:
        # 파일 추가
        subprocess.run(
            ['git', 'add', '.'],
            check=True,
            capture_output=True
        )
        
        # 커밋 메시지 생성
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"자동 커밋: {script_path.name} 실행 ({timestamp})"
        
        # 커밋
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if commit_result.returncode == 0:
            print(f"✅ 커밋 완료: {commit_message}")
            
            # 커밋 해시 가져오기
            hash_result = subprocess.run(
                ['git', 'log', '-1', '--format=%h'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if hash_result.returncode == 0:
                commit_hash = hash_result.stdout.strip()
                print(f"📦 커밋 해시: {commit_hash}")
            
            return True
        else:
            print(f"⚠️  커밋 실패: {commit_result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python auto_commit_on_run.py <스크립트.py> [인자들...]")
        print()
        print("예제:")
        print("  python auto_commit_on_run.py 251220.py")
        print("  python auto_commit_on_run.py script.py arg1 arg2")
        sys.exit(1)
    
    script_path = sys.argv[1]
    args = sys.argv[2:]
    
    success = run_and_commit(script_path, *args)
    
    if success:
        print()
        print("=" * 60)
        print("✅ 완료!")
        print("=" * 60)
        print()
        print("💡 GitHub에 푸시하려면:")
        print("   git push")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

