#! /usr/bin/env python
#coding:utf-8
 
import sys
import re
import urllib2
import urllib
import requests
import cookielib

from bs4 import BeautifulSoup
 
## 这段代码是用于解决中文报错的问题  
reload(sys)  
sys.setdefaultencoding("utf8")  
#####################################################
loginurl = 'http://www.lintcode.com/zh-cn/accounts/signin/'
domain = 'http://www.lintcode.com/'
 
class xSpider(object):
	 
	def __init__(self):
		'''initiation'''
		
		self.name = ''
		self.passwprd = ''
 
		self.cj = cookielib.LWPCookieJar()            
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)) 
		urllib2.install_opener(self.opener)    
	 
	def setLoginInfo(self,username,password):
		'''set user information'''
		self.name = username
		self.pwd = password

	def preLogin(self):
		'''to get csrfmiddlewaretoken'''
		req = urllib2.Request('http://www.lintcode.com/accounts/signin/')
		req.add_header('Host','www.lintcode.com')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		content = response.read().decode('utf-8')

		pattern = re.compile('<input.*?csrfmiddlewaretoken.*?/>')
		item = re.findall(pattern, content)
#		print item[0]
		print 'get csrfmiddlewaretoken success!'
		return item[0][item[0].find('value=') + 7 : -4]
		
 
	def login(self, csrfmiddlewaretoken):
		'''login'''
		loginparams = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'username_or_email':self.name, 'password':self.pwd}
		req = urllib2.Request(loginurl, urllib.urlencode(loginparams))
		req.add_header('Host','www.lintcode.com')
		req.add_header('Origin','http://www.lintcode.com')
		req.add_header('Referer','http://www.lintcode.com/zh-cn/accounts/signin/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		thePage = response.read()
		print 'login success!'
#		print thePage

	def getSubmissionId(self, questionName):
		'''download each question'''
		quesURL = domain + 'zh-cn/problem/' + questionName + '/submissions/'
		req = urllib2.Request(quesURL)
		req.add_header('Host','www.lintcode.com')
		req.add_header('Origin','http://www.lintcode.com')
		req.add_header('Referer','http://www.lintcode.com/zh-cn/accounts/signin/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		submissionPage = response.read()
		submissionPage =submissionPage.replace('\n','')
		print submissionPage
		soup = BeautifulSoup(submissionPage)
		print soup.find_all('a', text = '            Accepted        ')

		 
if __name__ == '__main__':
	userlogin = xSpider()
	username = 'xiaoyifeibupt'
	password = 'x1a0ya0'
	userlogin.setLoginInfo(username,password)
	csrfmiddlewaretoken = userlogin.preLogin()
	userlogin.login(csrfmiddlewaretoken)
	userlogin.getSubmissionId('find-the-missing-number')