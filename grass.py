import auto_push

# data 각 행의 합계와 전체 총합을 이중 for문을 사용해 출력해보자.

data = [
    [80, 40, 14, 15, 45, 47, 45, 45, 78, 20],
    [70, 60, 55, 75, 95, 90, 80, 80, 85, 100],  
    [20, 28, 40, 70, 70, 20, 20, 70, 70, 80]
]

total = 0

for i in range(len(data)):
    row_sum = 0
    for j in range(len(data[i])):
        row_sum += data[i][j]
        total   += data[i][j]
    print(f'data[{i}] {row_sum}')
print(total)