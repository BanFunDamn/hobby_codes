#! /usr/bin/env python3

import adjust_html
import datetime, os

def get_date():
  tmp_date = datetime.datetime.now()
  month = str(tmp_date.month)
  if len(month) == 1:
    month = "0" + month
  day = str(tmp_date.day)
  if len(day) == 1:
    day = "0" + day
  today = month + "/" + day
  return today

url_head = "https://seiga.nicovideo.jp"
url_body = "/manga/?track=global_navi_top"

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

def parse_href_tag(text):
  tmp = text.split("href=")[1]
  if tmp[0] == "\"":
    tmp = tmp.split("\"")[1]
  elif tmp[0] == "\'":
    tmp = tmp.split("\'")[1]
  return tmp

def get_updated_pages(url, date):
  adjust_html.main(url, "test/tmp.html")
  content = []
  with open("test/tmp.html") as rf:
    content = rf.read().split("\n")
  updated_page_list = {}
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
        img_link, name = parse_image_tag(full_link)
        while(True):
          if tmp_index == -1:
            break
          elif adjust_html.clean_spaces(content[tmp_index])[3:7] == "href":
            break
          else:
            tmp_index -= 1
        full_link = adjust_html.clean_spaces(content[tmp_index])
        link = parse_href_tag(full_link)
        updated_page_list[name] = link
  os.remove("test/tmp.html")
  return updated_page_list

def get_updated_comics(url, date):
  adjust_html.main(url, "test/tmp.html")
  content = []
  with open("test/tmp.html") as rf:
    content = rf.read().split("\n")
  updated_comic_list = {}
  for i in range(len(content)):
    tmp_text = adjust_html.clean_spaces(content[i])
    if len(tmp_text) > 5:
      if date == tmp_text[:5]:
        tmp_index = i
        while(True):
          if tmp_index == -1:
            break
          elif adjust_html.clean_spaces(content[tmp_index])[10:27] == "serial_item_title":
            break
          else:
            tmp_index -= 1
        while(True):
          if "<" not in adjust_html.clean_spaces(content[tmp_index]):
            break
          else:
            tmp_index += 1
        name = adjust_html.clean_spaces(content[tmp_index])
        while(True):
          if tmp_index == i:
            tmp_index = None
            break
          if adjust_html.clean_spaces(content[tmp_index])[10:28] == "latest_episode_box":
            break
          else:
            tmp_index += 1
        if tmp_index == None:
          continue
        full_link = adjust_html.clean_spaces(content[tmp_index])
        link = parse_href_tag(full_link)
        updated_comic_list[name] = link
  os.remove("test/tmp.html")
  return updated_comic_list

def create_database_html(dic_of_url, file_name):
  sentence = ["<!DOCTYPE html>",
              "<html lang=\"ja\">",
              "<head>",
              "<meta charset=\"UTF-8\">",
              "<title>新エピソード一覧</title>",
              "</head>",
              "<body>",
              "</body>",
              "</html>"
              ]
  for key in dic_of_url.keys():
    tmp = "<a href=\"" + dic_of_url[key] + "\">" + key + "</a><br>"
    sentence = sentence[:-2] + [tmp] + sentence[-2:]
  with open(file_name, mode="w") as wf:
    for line in sentence:
      wf.write(line + "\n")

if __name__ == "__main__":
  link_list = get_updated_pages(url_head + url_body, get_date())
  for key in link_list.keys():
    link_list[key] = url_head + link_list[key]
  check_list = []
  full_comic_list = {}
  for key in link_list.keys():
    comic_list = get_updated_comics(link_list[key], get_date())
    for ck in comic_list.keys():
      if ck not in check_list:
        full_comic_list.update({ck: url_head + comic_list[ck]})
        check_list += [ck]
  file_name = "test/data.html"
  create_database_html(full_comic_list, file_name)
  os.system("open -a Google\ Chrome " + file_name)
