import auto_push

name = ["전문준", "김민수", "이영희"]
korean = [90, 85, 95]
english = [85, 90, 80]
for name, korean, english in zip(name, korean, english):
    print(f"{name}: {korean} {english}")
