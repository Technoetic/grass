"""
Cursor IDE가 Git을 인식하도록 도와주는 스크립트
"""
import os
import json
from pathlib import Path
import subprocess


def get_git_path():
    """Git 실행 파일 경로 찾기"""
    try:
        result = subprocess.run(
            ['where.exe', 'git'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            git_path = result.stdout.strip().split('\n')[0]
            return git_path
    except:
        pass
    
    # 기본 경로 확인
    default_paths = [
        r'C:\Program Files\Git\cmd\git.exe',
        r'C:\Program Files (x86)\Git\cmd\git.exe',
    ]
    
    for path in default_paths:
        if Path(path).exists():
            return path
    
    return None


def check_cursor_settings():
    """Cursor 설정 확인"""
    # Cursor 설정 파일 경로
    app_data = os.getenv('APPDATA')
    cursor_settings_path = Path(app_data) / 'Cursor' / 'User' / 'settings.json'
    
    if cursor_settings_path.exists():
        try:
            with open(cursor_settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            return settings, cursor_settings_path
        except:
            pass
    
    return None, cursor_settings_path


def update_cursor_settings(git_path):
    """Cursor 설정에 Git 경로 추가"""
    settings, settings_path = check_cursor_settings()
    
    if settings is None:
        settings = {}
    
    # Git 경로 설정
    if 'git.path' not in settings or settings['git.path'] != git_path:
        settings['git.path'] = git_path
        settings['git.enabled'] = True
        
        # 설정 파일 디렉토리 생성
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 설정 저장
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        return True
    
    return False


def main():
    """메인 함수"""
    print("=" * 60)
    print("Cursor IDE Git 인식 설정")
    print("=" * 60)
    print()
    
    # Git 경로 찾기
    print("1️⃣ Git 경로 확인 중...")
    git_path = get_git_path()
    
    if not git_path:
        print("❌ Git을 찾을 수 없습니다.")
        print("   Git이 설치되어 있는지 확인하세요.")
        return
    
    print(f"✅ Git 발견: {git_path}")
    print()
    
    # Git 버전 확인
    try:
        result = subprocess.run(
            [git_path, '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            print(f"✅ Git 버전: {result.stdout.strip()}")
    except:
        pass
    
    print()
    
    # Cursor 설정 업데이트
    print("2️⃣ Cursor 설정 업데이트 중...")
    updated = update_cursor_settings(git_path)
    
    if updated:
        print("✅ Cursor 설정이 업데이트되었습니다!")
        print()
        print("⚠️  중요: Cursor IDE를 재시작해야 합니다.")
        print("   - Cursor를 완전히 종료")
        print("   - 다시 실행")
        print("   - 또는 Ctrl + Shift + P → 'Reload Window'")
    else:
        print("ℹ️  Cursor 설정이 이미 올바르게 설정되어 있습니다.")
        print()
        print("만약 여전히 Git을 인식하지 못한다면:")
        print("   1. Cursor를 재시작하세요")
        print("   2. 또는 Ctrl + Shift + P → 'Reload Window'")
    
    print()
    print("=" * 60)
    print("설정 완료!")
    print("=" * 60)


if __name__ == '__main__':
    main()


