#coding: utf-8
import os
import re
from ast import literal_eval
from bs4 import BeautifulSoup
import datetime

try:
	import win32com.client
except ImportError:
	print('缺少pypiwin32库，请自行pip install pypiwin32')
	exit(0)
	# 如果你使用了某些代理软件可以取消注释下四行并正确设置后重新运行
	# console = 'set http_proxy=http://127.0.0.1:1080'
	# os.popen(console).read()
	# console = 'set https_proxy=http://127.0.0.1:1080'
	# os.popen(console).read()
	console = 'pip install pypiwin32'
	line = os.popen(console).read()
	print(line)
	import win32com.client
	


def encodingconv(ustr):
	uresult = str(eval(repr(literal_eval("b'{}'".format(ustr)))), "gbk")
	return uresult

def extract(mailname):
	emaildict = {}
	outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
	msg = outlook.OpenSharedItem(mailname)
	mailbody = msg.Body
	cjdw = re.findall(r"承接单位：\w+", mailbody)[0].replace('\r\n', '').split('：')
	ysje = re.findall(r"应收总额：\d+\.?\d*元", mailbody)[0].replace('\r\n', '').split('：')
	xmmc = re.findall(r"项目名称：\s*\w+\s*", mailbody)[0].replace(' ','').replace('\r\n', '').split('：')
	cjrq = re.findall(r"承接日期：\d+/\d+/\d+", mailbody)[0].replace('\r\n', '').split('：')
	emaildict[cjdw[0]] = cjdw[1]
	emaildict[ysje[0]] = ysje[1]
	emaildict[xmmc[0]] = xmmc[1]
	emaildict[cjrq[0]] = cjrq[1]
	del outlook, msg
	return emaildict

mails = [mail for mail in os.listdir() if mail.endswith('.msg')]

havechangelist = []
errorlist = []

mail = '2017年--考试对账单.msg'
for mail in mails:
	try:
		maildict = extract(os.getcwd() + '\\' + mail)
		date = datetime.datetime.strptime(maildict['承接日期'], ("%m/%d/%Y")).strftime('%Y%m%d')
		rst = date + maildict['项目名称'] + maildict['承接单位'] + re.findall(r"\d+\.?\d*", maildict['应收总额'])[0] + '元'
		if rst not in havechangelist:
			print('将' + mail + '更改为' + rst +'.msg')
			console = 'ren \"' + mail + '\"  \"' + rst + '.msg\"'
			print(console)
			line = os.popen(console).read()
			print(line)
			havechangelist.append(rst)
		else:
			errorlist.append(rst)
	except Exception:
		errorlist.append(rst)

print(errorlist)