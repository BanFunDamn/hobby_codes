import datetime, os

site_list = {# URL in key, moment in value
             # write several moments dividing by comma
             "https://comic-walker.com/":"Everyday",
             "https://web-ace.jp/youngaceup/contents/":"Everyday",
             "https://www.alphapolis.co.jp/manga/official":"Everyday",
             "https://comic-boost.com/series?action=index&controller=gentosha%2Fseries&new_series=true&per=60":"Everyday",
             "https://futabanet.jp/list/monster/serial":"Everyday",
             "https://www.ganganonline.com/contents/":"Monday,Thursday",
             "https://www.comic-earthstar.jp/":"Thursday",
             "http://comicride.jp/":"Thursday",
             "http://hobbyjapan.co.jp/comic/series/":"Friday",
             "https://comic-gardo.com/":"Friday",
             "http://storia.takeshobo.co.jp/":"Friday",
             "https://gammaplus.takeshobo.co.jp/index.html":"Friday",
             "https://comic.mag-garden.co.jp/":"5th",
             "https://webcomicgamma.takeshobo.co.jp/":"10th",
             }

app = "Brave Browser"

def update_today(keyword): # check the keyword type
  if keyword == "Everyday":
    return True
  elif "day" in keyword:
    return update_day(keyword)
  elif "th" in keyword:
    return update_date(keyword)
  else:
    return False

def update_day(days):
  day_list = days.split(",")
  today = datetime.datetime.now().strftime('%A')
  for day in day_list:
    if day == today:
      return True
  return False

def update_date(dates):
  date_list = dates.split(",")
  today = datetime.datetime.now().day
  for date in date_list:
    if int(today) % int(date.replace("th","")) == 0:
      return True
  return False

def open_site(url, app):
  os.system("open -a \"" + app + "\" " + url)

def main(site_list, app):
  for key in site_list.keys():
    if update_today(site_list[key]):
      open_site(key, app)

if __name__ == "__main__":
  main(site_list, app)
