#-*- coding:utf-8 -*-
import requests
url = 'http://select.pdgzf.com/'
r = requests.get(url)

url_yzm = 'http://select.pdgzf.com/ValidationImage.aspx'
for i in xrange(100):
    r1 = requests.get(url_yzm)
    if r1.status_code == requests.codes.ok:
        with open('yzm/yzm'+bytes(i)+'.jpg','wb') as fd:
            for chunk in r1.iter_content(100):
                fd.write(chunk)