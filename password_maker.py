#!python3

def pw_maker():
  import random
  length = int(input("PW_length: "))
  pw = ""
  rule = [[10, 48], [26, 97], [26, 65], [0,46]]
  ty = []
  style = int(input("1. 数字のみ\n2. 数字+小文字\n3. 数字+小文字+大文字\n4. 数字+小文字+大文字+記号\n"))
  while(True):
    for i in range(length):
      tmp = int(random.random() * 8)
      if style == 1:
        ty += [0]
      elif style == 2:
        if tmp < 3:
          ty += [0]
        else:
          ty += [1]
      else:
        if tmp < 2:
          ty += [0]
        elif tmp < 5:
          ty += [1]
        else:
          ty += [2]
    if style == 4:
      point = int(random.random() * len(ty))
      ty[point-1] = 3
    check = True
    for i in range(style):
      if i not in ty:
        check = False
        break
    if check:
      break
    else:
      ty = []
  for i in range(len(ty)):
    pw += chr(int(random.random() * rule[ty[i]][0]) + rule[ty[i]][1])
  return pw

if __name__ == "__main__":
  print(pw_maker())
