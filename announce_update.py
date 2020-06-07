#! /usr/bin/env python3

import adjust_html
import time

newest = ""
reload_interval = 3600

while(True):
	output = "test/test.html"
	adjust_html.main("https://japanese.engadget.com", output)
	focusing = []
	flag = False
	with open(output) as rf:
		for line in rf.read().split("\n"):
			tmp = adjust_html.clean_spaces(line)
			if len(tmp) != 0:
				if tmp[0] != "<":
					if "最新記事" in tmp:
						flag = True
					elif "もっと読む" in tmp:
						flag = False
					elif flag:
						focusing += [tmp]
	if newest != focusing[0]:
		i = input("New Info!!!\nRefresh? [y/N] ")
		if i == "y":
			newest = focusing[0]
	time.sleep(reload_interval)
