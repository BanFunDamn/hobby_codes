#! /usr/bin/env python3

import adjust_html
import datetime

def get_date():
  tmp_date = datetime.datetime.now()
  month = str(tmp_date.month)
  if len(month) == 1:
    month = "0" + month
  day = str(tmp_date.day)
  if len(month) == 1:
    day = "0" + day
  today = month + "/" + day
  return today

url = "https://seiga.nicovideo.jp/manga/?track=global_navi_top"

def parse_image_tag(text):
  tmp = text
  if "<img " in tmp[:5]:
    tmp = tmp[5:]
  if ">" in tmp[-1]:
    tmp = tmp[:-1]
  if "/" in tmp[-1]:
    tmp = tmp[:-1]
  if "\"" in tmp:
    tmp = tmp.replace("\"", "")
  if "\'" in tmp:
    tmp = tmp.replace("\'", "")
  alt, src, title = tmp.split(" ")
  if "alt=" in alt[:4] and "src=" in src[:4] and "title=" in title[:6]:
    src = src[4:]
    title = title[6:]
  return src, title

def get_updated_pages(url, date):
  adjust_html.main(url, "test/tmp.html")
  content = []
  with open("test/tmp.html") as rf:
    content = rf.read().split("\n")
  updated_page_list = []
  for i in range(len(content)):
    tmp_text = adjust_html.clean_spaces(content[i])
    if len(tmp_text) > 5:
      if date == tmp_text[:5]:
        tmp_index = i
        while(True):
          if tmp_index == -1:
            break
          elif adjust_html.clean_spaces(content[tmp_index])[1:4] == "img":
            break
          else:
            tmp_index -= 1
        full_link = adjust_html.clean_spaces(content[tmp_index])
        link, name = parse_image_tag(full_link)
        updated_page_list += [f"{name} [{link}]"]
  for page in updated_page_list:
    print(page)

get_updated_pages(url, get_date())
