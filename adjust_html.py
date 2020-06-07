def clean_spaces(text): # 文字列先頭に並ぶ半角スペースを除外
  tmp_text = text
  while(True):
    if len(tmp_text) == 0:
      return tmp_text
    elif tmp_text[0] != " ":
      return tmp_text
    else:
      tmp_text = tmp_text[1:]

def pop_word(text): # htmlデータの文字とタグを分離（先頭がタグでない場合有効）
  tmp_text = text
  border = tmp_text.index("<")
  tmp_word = tmp_text[:border]
  tmp_tag = tmp_text[border:]
  return tmp_tag, tmp_word

def pop_tag(text): # htmlデータの先頭のタグとそれ以降を分離（先頭がタグの場合有効）
  tmp_text = text
  border = tmp_text.index(">")
  tmp_tag = tmp_text[:border + 1]
  tmp_word = tmp_text[border + 1:]
  return tmp_tag, tmp_word

def adjust_indent(tag): # タグによるインデント調整
  if tag[0] != "<":
    return None
  if tag[1] == "/": # 閉じタグの場合（例：</head>）
    return -1
  if tag[1] != "/" and tag[-2] == "/": # 特殊タグの場合（例：<meta ~~ />）
    return 0
  if tag[1] == "!": # 特殊タグの場合（例：<!DOCTYPE ~~>）
    return 0
  else:
    return 1

def parse_html(writing_file, url, indent, point): # htmlデータのインデントを整える
  content = clean_spaces(url)
  if len(content) == 0:
    return indent
  if content[0] == "<":
    tag, word = pop_tag(content)
    check = adjust_indent(tag)
    if check != 1:
      writing_file.write(f"{' ' * (indent + check) * point}{tag}\n")
    else:
      writing_file.write(f"{' ' * indent * point}{tag}\n")
    return parse_html(writing_file, word, indent + check, point)
  else:
    tag, word = pop_word(content)
    writing_file.write(f"{' ' * indent * point}{word}\n")
    return parse_html(writing_file, tag, indent, point)

def main(url, filename):
  import requests, bs4

  web = url

  wf = open(filename, mode = "w")  

  get_url_info = requests.get(web)
  bs4Obj = bs4.BeautifulSoup(get_url_info.text, "lxml")
  webContent = str(bs4Obj)
  
  i = 0
  flag = False
  for wc in webContent.split("\n"):
    content = wc
    while(True):
      if len(content) == 0:
        break
      elif content[0] != " ":
        break
      else:
        content = content[1:]
    if content != "":
      div = content.split(">")
      for x in range(len(div) - 1):
        i = parse_html(wf, div[x] + ">", i, 2)
  wf.close()

if __name__ == "__main__":
  import sys
  url = ""
  filename = ""
  try:
    url = sys.argv[1]
  except:
    url = "https://japanese.engadget.com" # 初期URL
  try:
    filename = sys.argv[2]
  except:
    filename = "output.html" # 初期出力ファイル名
  main(url, filename)
