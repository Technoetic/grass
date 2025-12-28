import auto_push

def create_profile(**info):
    print("=== 인 적 사 항 ===")
    for key, value in info.items():
        print(f"{key}: {value}")

create_profile(이름 = "김철수", 나이 = 30, 직업 = "개발자", 취미 = "독서")