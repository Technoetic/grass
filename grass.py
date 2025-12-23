import auto_push

coffee = 10
money = 300

while True:
    money = int(input("돈을 넣어주세요: "))
    if money == 300:
        print("커피를 줍니다.")
        coffee = coffee - 1
    elif money > 300:
        print(f"거스름 돈 {money - 300}를 주고 커피를 줍니다.")
        coffee = coffee - 1
    else:
        print(f"남은 커피의 양은 {coffee}개입니다.")
    if coffee == 0:
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")
        break


print(money)