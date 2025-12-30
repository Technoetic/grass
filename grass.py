import auto_push

# 다음 2차원 리스트 data가 주어졌을 때, 이중 for문을 사용하여 아래 내용을 출력해보세요.

# 구현할 내용
# data[0], data[1], data[2] 각각의 최댓값과 최솟값 출력
# data 전체에서의 최댓값과 최솟값 출력

data = [
    [80, 40, 14, 15, 45, 47, 45, 45, 78, 20],
    [70, 60, 55, 75, 95, 90, 80, 80, 85, 100],
    [20, 28, 40, 70, 70, 20, 20, 70, 70, 80]
]

all_max = data[0][0]
all_min = data[0][0]

for i in range(len(data)):
    row_max = data[i][0]
    row_min = data[i][0]

    for j in range(len(data[i])):
        v = data[i][j]

        if v > row_max:
            row_max = v
        if v < row_min:
            row_min = v

        if v > all_max:
            all_max = v
        if v < all_min:
            all_min = v
    print(f'data[{i}] max:{row_max} min:{row_min}')

print(f'max:{all_max} min:{all_min}')
