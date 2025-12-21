from auto_push import auto_commit_and_push

# 메인 로직 실행
n = int(input())
result = sum(range(1, n+1))
print(result)

# 실행 후 자동으로 git push 수행
auto_commit_and_push(script_name='grass.py')