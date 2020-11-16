#! /usr/bin/env python3
# pip3 install requests beautifulsoup4 lxml

import adjust_html
import datetime, os

def get_date(tmp_date):
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
  # alt, src, title = tmp.split(" ")
  # if "alt=" in alt[:4] and "src=" in src[:4] and "title=" in title[:6]:
  #   src = src[4:]
  #   title = title[6:]
  tmp_datas = tmp.split(" ")
  alt = ""
  src = ""
  title = ""
  for td in tmp_datas:
    if "alt=" in td[:4]:
      alt = td[4:]
    if "src=" in td[:4]:
      src = td[4:]
    if "title=" in td[:6]:
      title = td[6:]
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
  flag = True
  for i in range(len(content)):
    if "Forbidden" in content[i] and "403" in content[i]:
      flag = False
      break
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
  return updated_page_list, flag

def get_updated_comics(url, date, database):
  adjust_html.main(url, "test/tmp.html")
  content = []
  with open("test/tmp.html") as rf:
    content = rf.read().split("\n")
  updated_comic_list = {}

  database_key = []
  with open(database) as rf:
    for line in rf.read().split("\n"):
      if "href" in line[:7]:
        key = line.split(">")[1].split("<")[0]
        database_key += [key]
      elif "<!--" in line[:4]:
        key = line.replace("<!-- ", "").replace(" -->", "").split(", date:")[0]
        database_key += [key]

  flag = True
  for i in range(len(content)):
    if "Forbidden" in content[i] and "403" in content[i]:
      flag = False
      break
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

        if name not in database_key:
          updated_comic_list[name] = link

#        updated_comic_list[name] = link
  os.remove("test/tmp.html")
  return updated_comic_list, flag

def create_database_html(dic_of_url, file_name, date):
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
  count = 0
  for key in dic_of_url.keys():
    tmp = "<a href=\"" + dic_of_url[key] + "\">" + key + "</a><br>"
    sentence = sentence[:-2] + [tmp] + sentence[-2:]
    count += 1

  old_database = {}
  with open(file_name) as rf:
    for line in rf.read().split("\n"):
      if "href" in line[3:7]:
        key = line.split(">")[1].split("<")[0]
        old_database.update({key: date})
      elif "<!--" in line[:4]:
        keys = line.replace("<!-- ", "").replace(" -->", "").split(", date:")
        old_database.update({keys[0]: keys[1]})
  for key in old_database.keys():
    if old_database[key] == date or count == 0:
      tmp = "<!-- " + key + ", date:" + old_database[key] + " -->"
      sentence = sentence[:-2] + [tmp] + sentence[-2:]

  with open(file_name, mode="w") as wf:
    for line in sentence:
      wf.write(line + "\n")

def main(log_name):
  os.system("touch \"" + log_name + "\"")
  contents = []
  with open("log") as rf:
    contents = rf.readlines()
  content = ""
  index = -1
  for i in range(len(contents)):
    if "NicoNico: " in contents[i]:
      content = contents[i].replace("NicoNico: ", "")
      index = i
    if contents[i][-1] != "\n":
      contents[i] += "\n"
  if content == "":
    content = "1111-11-11 11:11:11.111111\n"
  last_check = datetime.datetime.strptime(content, '%Y-%m-%d %H:%M:%S.%f\n')
  tmp_date = datetime.datetime.now()
  if tmp_date.time() < datetime.time(12, 0, 0):
    tmp_date = tmp_date - datetime.timedelta(1)
  if last_check.time() < datetime.time(12, 0, 0):
    last_check = last_check - datetime.timedelta(1)
#  if tmp_date.date() > last_check.date():
  if tmp_date.date() >= last_check.date():
    today = get_date(tmp_date)
    while(True):
      link_list, collect_flag = get_updated_pages(url_head + url_body, today)
      if collect_flag:
        break
    for key in link_list.keys():
      link_list[key] = url_head + link_list[key]
    check_list = []
    full_comic_list = {}
    file_name = "test/niconico.html"
    os.system("touch \"" + file_name + "\"")
    for key in link_list.keys():
      comic_list, collect_flag = get_updated_comics(link_list[key], today, file_name)
      while(True):
        if collect_flag:
          break
        comic_list, collect_flag = get_updated_comics(link_list[key], today, file_name)
      for ck in comic_list.keys():
        if ck not in check_list:
          full_comic_list.update({ck: url_head + comic_list[ck]})
          check_list += [ck]
    create_database_html(full_comic_list, file_name, today)
    os.system("open -a \"Brave Browser\" " + file_name)
  if index != -1:
    contents[index] = "NicoNico: " + str(datetime.datetime.now()) + "\n"
  else:
    contents += ["NicoNico: " + str(datetime.datetime.now()) + "\n"]
  with open("log", mode="w") as wf:
    for i in range(len(contents)):
      wf.write(contents[i])

if __name__ == "__main__":
  main("log")
