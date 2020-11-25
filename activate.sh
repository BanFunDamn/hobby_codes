#! /bin/bash

niconico="niconico.html"

git pull >& /dev/null

python3 check_niconico_update.py -o $niconico
python3 auto_open_manga_site.py

git add niconico.html
git add log
git commit -m "log updated" >& /dev/null
git push origin master >& /dev/null
