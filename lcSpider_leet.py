#! /usr/bin/env python
#coding:utf-8
 
import sys
import re
import urllib2
import urllib
import requests
import cookielib

import lxml.html.soupparser as soupparser


## 这段代码是用于解决中文报错的问题  
reload(sys)  
sys.setdefaultencoding("utf8")  
#####################################################

domain = 'https://leetcode.com/'
 
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
		
		req = urllib2.Request('https://leetcode.com/accounts/login/')
		req.add_header('Host','leetcode.com')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		login_page = response.read()

		dom = soupparser.fromstring(login_page)
		csrfmiddlewaretoken = dom.xpath("//*[@name='csrfmiddlewaretoken']/@value")[0]

		print 'get csrfmiddlewaretoken success!'
		return csrfmiddlewaretoken
		
 
	def login(self, csrfmiddlewaretoken):
		
		'''login'''
		loginurl = 'https://leetcode.com/accounts/login/'		
		loginparams = {'csrfmiddlewaretoken':csrfmiddlewaretoken,'login':self.name, 'password':self.pwd}
		
		req = urllib2.Request(loginurl, urllib.urlencode(loginparams))
		
		req.add_header('Host','leetcode.com')
		req.add_header('Origin','https://leetcode.com')
		req.add_header('Referer','https://leetcode.com/accounts/login/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		thePage = response.read()		
		print 'login success!'
		return thePage

	def getAcceptedQuetionList(self, problem_page):
		
		'''get Accepted Quetion List'''
		
		problem_urls = soupparser.fromstring(problem_page).xpath("//tr[td/span/@class='ac']/td[2]/a/@href")
		if not problem_urls:
			print "problems cannot be found. Username or password may not be right"
			sys.exit(-1)
		problems = map(lambda url:url.split('/')[-2],problem_urls)
		print 'getAcceptedQuetionList success'
		return problems

	def getSubmissionId(self, questionName):
		
		'''download each submission question id'''

		quesURL = domain + 'problems/' + questionName + '/submissions/'
		req = urllib2.Request(quesURL)
		req.add_header('Host','leetcode.com')
		req.add_header('Origin','https://leetcode.com')
		req.add_header('Referer','https://leetcode.com/accounts/login/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		submissionPage = response.read()

		results = soupparser.fromstring(submissionPage).xpath("//a[contains(@class,'status-accepted')]/@href")
		if not results:
			print 'accepted submission cannot be found on the first page'
			return
		
		return results[0]

	def getCode(self, submissionId):

		'''get description and code'''

		codeURL = domain + submissionId
		req = urllib2.Request(codeURL)
		req.add_header('Host','leetcode.com')
		req.add_header('Origin','https://leetcode.com')
		req.add_header('Referer','https://leetcode.com/accounts/login/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		codePage = response.read()
		
		match_results = re.search("scope.code.cpp[^']*'([^']*)'",codePage)
		code = match_results.group(1).decode('unicode-escape')
		with open(problem_name+'.cpp','w') as w:
			w.write(code)

		 
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage ./lcSpider.py USERNAME PASSWORD'
		sys.exit(0)
	userSpider = xSpider()
	
	username = sys.argv[1]
	password = sys.argv[2]
	
	userSpider.setLoginInfo(username,password)
	
	csrfmiddlewaretoken = userSpider.preLogin()

	questionPage = userSpider.login(csrfmiddlewaretoken)

	print questionPage

#	acceptedQuetionList = userSpider.getAcceptedQuetionList(questionPage)

#	count = 0

#	for acceptedQuetion in acceptedQuetionList:
#		count += 1
#		submissionId = 	userSpider.getSubmissionId(acceptedQuetion)
#		description, myCode = userSpider.getCode(submissionId)
#		
#		codeFile = open('lintcode/' + acceptedQuetion[9:] + '.cpp', 'w')
#		codeFile.write(description)
#		codeFile.write(str(myCode).replace('\\n','\n'))
#		codeFile.close
#		if count % 5 == 0:
#			print count


