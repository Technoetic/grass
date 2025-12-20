# 사용자로부터 정수 하나를 입력받아 n에 저장
n = int(input())
# 합계를 저장할 변수, 0으로 초기화
total = 0
# i가 1부터 n까지 1씩 증가하며 반복
# range(1, n+1)은 [1, 2, 3, ..., n] 을 의미
for i in range(1, n+1):
    # 현재 i 값을 total에 누적해서 더함
    # total = total + i 와 같은 의미
    total += i
# 최종 합계 출력
print(total)