# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE, formatdate
from email import encoders

import os,time
import codecs

# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]):
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    for file in files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()

def sendMailToMe(text):
    server = {}
    server['name'] = 'smtp.163.com'  # 如果是写自己公司的邮件服务器，请使用IP的方式，不然会有DNS解析的问题
    # server['name'] = '123.125.50.135:25'
    server['user'] = 'snowflakeyhk@163.com'  # 用户名
    server['passwd'] = '19890512snow'  # 密码
    fro = 'snowflakeyhk@163.com'
    to = ['13764991541@139.com']
    subject = "gzf email "
    send_mail(server, fro, to, subject, text)


def searchGzf():
    # searchList = ['川周公路2880弄（康桥旭辉）','大道站路94弄（代理经租）','东波路192弄','东波路248弄',
    #               '东书房路390弄（代理经租）','东书房路560弄（代理经租）','公租房艾东苑','利津路51弄',
    #               '妙川路800弄（川沙博景苑）',
    #               '齐爱路168弄183单元','秋亭路88弄（朗诗未来树）',
    #               '上南路3880弄','宣黄公路2585弄（惠南宝业华庭）','杨南路694弄','永泰路136弄',
    #               '玉兰路60弄','枣庄路1029弄']
    searchList = [u'川周公路2880弄（康桥旭辉）',u'大道站路94弄（代理经租）',u'东波路192弄',u'东波路248弄',
                  u'东书房路390弄（代理经租）',u'东书房路560弄（代理经租）',u'公租房艾东苑',u'利津路51弄',
                  #u'妙川路800弄（川沙博景苑）',
                  u'齐爱路168弄183单元',u'秋亭路88弄（朗诗未来树）',
                  u'上南路3880弄',u'宣黄公路2585弄（惠南宝业华庭）',u'杨南路694弄',u'永泰路136弄',
                  u'玉兰路60弄',u'枣庄路1029弄']

    cookie_str = 'fwb0pgbuhp2b1xyxpbs2mrz3'
    req = requests.Session()
    core_url1 = 'http://select.pdgzf.com/Admin/personalSelect.aspx'
    core_header1 = {'Host': 'select.pdgzf.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://select.pdgzf.com/',
                    'Cookie': 'ASP.NET_SessionId='+cookie_str,
                    'Connection': 'keep-alive'}
    sendMail = 0
    status = 0 # 0: ok  1:not login
    for dizhi in searchList:
        time.sleep(1)
        strToSend = u''
        payload = {'xm':dizhi}
        r4 = req.get(core_url1,headers = core_header1,params=payload)
        #print r4.text
        #print dizhi
        soup = BeautifulSoup(r4.text,'lxml')
        chapter_list = soup.find_all("ol", class_="list")
        if chapter_list.__len__() != 1:
            print "not login!"
            status = 1
            break
        else:
            target = soup.find("ol", class_="list")
            str = dizhi + u'有'+bytes(target.find_all('li').__len__())+u'套房子！'
            if target.find_all('li').__len__() > 0:
                with codecs.open(dizhi+u'.html', 'w',encoding='utf-8') as f:
                    f.write(r4.text)
                strToSend = strToSend + str

            if len(strToSend) > 0:
                sendMailToMe(strToSend)
                #print strToSend
                sendMail = 1
                print "mail send!"
                print 'content:'+strToSend

    return status,sendMail


if __name__ == '__main__':
    iter = 0
    ISOTIMEFORMAT ='%Y - %m - %d %X'
    while(1):
        status,sendMail =  searchGzf()
        iter += 1
        print "search loop "+bytes(iter)+" end at "+time.strftime(ISOTIMEFORMAT, time.localtime( time.time() ) )
        if sendMail==1 or status==1:
            break
        time.sleep(20)

    print "end"