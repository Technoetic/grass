import auto_push

s1 = set([1, 2, 3, 4, 5])
s2 = set([3, 4, 5, 6, 7])

s1.add(199)

s1.update(s2)

print(s1)