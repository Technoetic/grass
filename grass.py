import auto_push

name = ["전문준", "김민수", "이영희"]
score = [90, 85, 95]
for name, score in zip(name, score):
    print(f"{name}: {score}")