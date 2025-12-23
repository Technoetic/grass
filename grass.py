import auto_push

count = 0
while count < 5:
    if count == 3:
        break
    print(f"count: {count}")
    count = count + 1
else:
    print("while문이 종료되었습니다.")