import auto_push

def say_myself(name, age, man = True):
    print("나의 이름은 %s입니다." % name)
    print("나이는 %d살입니다." % age)
    if man:
        print("남자입니다.")

    else:
        print("여자입니다.")

    say_myself("전문준, 88, True")