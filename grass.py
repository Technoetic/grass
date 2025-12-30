import auto_push

# 이 문자열을 / 기준으로 분리(split)한 뒤, 리스트 txt에 append(추가) 하여 저장하시오.

pumMok = '노트북/모니터/키보드'

txt = []

txt.extend(pumMok.split('/'))

print(txt)