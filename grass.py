import auto_push

def print_kwargs(**kwargs):
    print(kwargs)

print_kwargs(a=1)

print_kwargs(name = "foo", age = 3)

print_kwargs(name = "전문준",  age = 88, city = "서울",  job = "개발자")