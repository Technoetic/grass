"""
Cursor IDE에서 사용하기 쉬운 커밋 헬퍼
간단한 명령어로 Git 커밋을 수행합니다.
"""
import sys
import argparse
from git_auto_commit import GitAutoCommit


def commit_command(message: str = None, push: bool = False, 
                  files: list = None):
    """커밋 명령어"""
    try:
        git = GitAutoCommit()
        result = git.auto_commit(message=message, push=push)
        
        if result['success']:
            print(f"✅ {result['message']}")
            if result.get('committed_files'):
                print(f"📝 커밋된 파일: {len(result['committed_files'])}개")
            if push and result.get('pushed'):
                print("🚀 푸시 완료")
        else:
            print(f"ℹ️  {result['message']}")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


def status_command():
    """상태 확인 명령어"""
    try:
        git = GitAutoCommit()
        status = git.check_status()
        branch = git.get_branch()
        
        print(f"🌿 브랜치: {branch}")
        print(f"📊 변경사항: {status['count']}개 파일")
        
        if status['has_changes']:
            print("\n변경된 파일:")
            for file in status['changed_files']:
                print(f"  {file}")
        else:
            print("✅ 커밋할 변경사항이 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


def log_command(count: int = 10):
    """커밋 로그 보기"""
    try:
        git = GitAutoCommit()
        commits = git.get_recent_commits(count)
        
        print(f"📜 최근 커밋 {len(commits)}개:\n")
        for commit in commits:
            print(f"  {commit['hash']} - {commit['message']}")
            print(f"    {commit['date']} by {commit['author']}\n")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='Cursor IDE용 Git 커밋 헬퍼',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예제:
  python commit_helper.py commit -m "업데이트"
  python commit_helper.py commit --push
  python commit_helper.py status
  python commit_helper.py log
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='명령어')
    
    # commit 명령어
    commit_parser = subparsers.add_parser('commit', help='커밋 수행')
    commit_parser.add_argument('-m', '--message', help='커밋 메시지')
    commit_parser.add_argument('-p', '--push', action='store_true', 
                              help='푸시도 함께 수행')
    
    # status 명령어
    subparsers.add_parser('status', help='저장소 상태 확인')
    
    # log 명령어
    log_parser = subparsers.add_parser('log', help='커밋 로그 보기')
    log_parser.add_argument('-n', '--count', type=int, default=10,
                           help='표시할 커밋 수')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'commit':
        commit_command(message=args.message, push=args.push)
    elif args.command == 'status':
        status_command()
    elif args.command == 'log':
        log_command(count=args.count)


if __name__ == '__main__':
    main()

