import auto_push

# 점수 리스트에서 90점 이상인 자료만 골라 합계와 평균을 구하라!

scores = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]

total = 0
count = 0

for i in scores:
    if i >= 90:
        total += scores
        count += 1

print(total)
print(count)