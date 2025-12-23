import auto_push

cnt = 1
even_sum = 0
odd_sum = 0

for _ in range(100):  # 100번 반복
    if cnt % 2 == 0:
        even_sum += cnt
    else:
        odd_sum += cnt
    cnt += 1

print("cnt =", cnt)          # 스크래치에선 마지막에 101이 됨
print("짝수 =", even_sum)     # 2+4+...+100
print("홀수 =", odd_sum)      # 1+3+...+99
