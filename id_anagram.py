from argparse import ArgumentParser
import random


def random_anagram(name):
  new = ""
  vowel = ["a", "e", "i", "o", "u"]
  for i in range(len(name)):
    if name[i] in vowel:
      new += vowel[int(random.random() * 5)]
    else:
      order = ord(name[i])
      order = order + int(random.random() * 11) - 6
      new += chr(order)
  return new

def main(name):
  new_id = random_anagram(name)
  print(new_id)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("name", help="source name")
  args = parser.parse_args()
  main(args.name)
