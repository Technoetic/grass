import auto_push

def mix_func(name, *args, **kwargs):
    print(f"이름: {name}")
    print(f"숫자 인수들: {args}")
    print(f"인적 인수들: {kwargs} ")

mix_func("전문준", 100, 101, age = 25, city = "서울")