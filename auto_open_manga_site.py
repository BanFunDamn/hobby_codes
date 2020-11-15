import datetime, os

site_list = {# URL in key, moment in value
             # write several moments dividing by comma
             "https://comic-walker.com/":"Everyday_12:00",
             "https://web-ace.jp/youngaceup/contents/":"Workday_12:00",
             "https://www.alphapolis.co.jp/manga/official":"Workday_12:00",
             "https://comic-boost.com/series?action=index&controller=gentosha%2Fseries&new_series=true&per=60":"Workday_12:00",
             "https://futabanet.jp/list/monster/serial":"Workday_12:00",
             "https://www.ganganonline.com/contents/":"Monday,Thursday_12:00",
             "https://www.comic-earthstar.jp/":"Thursday_18:00",
             "https://hobbyjapan.co.jp/comic/series/":"Friday_16:00",
             "https://comic-gardo.com/":"Friday_12:00",
             "http://storia.takeshobo.co.jp/":"Friday_12:00",
             "https://gammaplus.takeshobo.co.jp/index.html":"Friday_12:00",
             "https://comic.mag-garden.co.jp/":"5th_12:00",
             "https://webcomicgamma.takeshobo.co.jp/":"10th_12:00",
             "https://tonarinoyj.jp/episode/13932016480028985383":"Everyday_0:00",
             "https://shonenjumpplus.com/":"Everyday_0:00",
             "https://pash-up.jp/comic":"Workday_0:00",
             "https://pocket.shonenmagazine.com/":"Everyday_0:00",
             "https://www.comicbunch.com/":"Friday_0:00",
             "https://konomanga.jp/original":"Everyday_0:00",
             "https://www.comic-valkyrie.com/#lineup":"Tuesday,Friday_0:00",
             }

app = "Brave Browser"

def update_today(keyword, last): # check the keyword type
  last_check = last
  date, stime = keyword.split("_")
  today = datetime.datetime.now()
  time = datetime.time(int(stime.split(":")[0]), int(stime.split(":")[1]))
  if today.time() < time:
    today = today - datetime.timedelta(1)
  if last_check.time() < time:
    last_check = last_check - datetime.timedelta(1)
  if last_check.date() >= today.date():
    return False
  if date == "Everyday":
    return True
  if date == "Workday":
    return update_workday(today)
  elif "day" in date:
    return update_day(date, today)
  elif "th" in date:
    return update_date(date, today)
  else:
    return False

def update_workday(today):
  now = today.strftime('%A')
  if now not in ["Saturday", "Sunday"]:
    return True
  return False

def update_day(days, today):
  day_list = days.split(",")
  now = today.strftime('%A')
  for day in day_list:
    if day == now:
      return True
  return False

def update_date(dates, today):
  date_list = dates.split(",")
  now = today.day
  for date in date_list:
    if int(now) % int(date.replace("th","")) == 0:
      return True
  return False

def open_site(url, app):
  os.system("open -a \"" + app + "\" " + url)

def main(site_list, app, log_name):
  os.system("touch \"" + log_name + "\"")
  contents = []
  with open("log") as rf:
    contents = rf.readlines()
  content = ""
  index = -1
  for i in range(len(contents)):
    if "MangaSite: " in contents[i]:
      content = contents[i].replace("MangaSite: ", "")
      index = i
    if contents[i][-1] != "\n":
      contents[i] = contents[i] + "\n"
  if content == "":
    content = "1111-11-11 11:11:11.111111\n"
  last_check = datetime.datetime.strptime(content, '%Y-%m-%d %H:%M:%S.%f\n')
  for key in site_list.keys():
    if update_today(site_list[key], last_check):
      open_site(key, app)
  if index != -1:
    contents[index] = "MangaSite: " + str(datetime.datetime.now()) + "\n"
  else:
    contents += ["MangaSite: " + str(datetime.datetime.now()) + "\n"]
  with open("log", mode="w") as wf:
    for i in range(len(contents)):
      wf.write(contents[i])

if __name__ == "__main__":
  main(site_list, app, "log")
