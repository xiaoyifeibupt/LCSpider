#! /usr/bin/env python
#coding:utf-8
 
import sys
import re
import urllib2
import urllib
import requests
import cookielib

import json

from bs4 import BeautifulSoup

## 这段代码是用于解决中文报错的问题  
reload(sys)  
sys.setdefaultencoding("utf8")  
#####################################################

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
		print 'get csrfmiddlewaretoken success!'
		return item[0][item[0].find('value=') + 7 : -4]
		
 
	def login(self, csrfmiddlewaretoken):
		
		'''login'''
		loginurl = 'http://www.lintcode.com/zh-cn/accounts/signin/'		
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
		return thePage

	def getAcceptedQuetionList(self, questionPage):
		
		'''get Accepted Quetion List'''
		
		question_soup = BeautifulSoup(questionPage)
		questionList = question_soup.find('div', attrs={'class': 'list-group list'}).find_all('a')
		acceptedQuetionList = []
		for questionItem in questionList:
			if questionItem.get_text('|', strip=True).split('|')[1] == 'Accepted':
				acceptedQuetionList.append(questionItem.get('href'))
		print 'getAcceptedQuetionList success'
		return acceptedQuetionList

	def getSubmissionId(self, questionName):
		
		'''download each submission question id'''
		
		quesURL = domain + 'zh-cn' + questionName + '/submissions/'
		req = urllib2.Request(quesURL)
		req.add_header('Host','www.lintcode.com')
		req.add_header('Origin','http://www.lintcode.com')
		req.add_header('Referer','http://www.lintcode.com/zh-cn/accounts/signin/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		submissionPage = response.read()

		submission_soup = BeautifulSoup(submissionPage)
		hrefList = submission_soup.find('tbody').find_all('a')
		
		idhref = hrefList[0].get('href')
		return idhref

	def getCode(self, submissionId):

		'''get description and code'''

		codeURL = domain + submissionId
		req = urllib2.Request(codeURL)
		req.add_header('Host','www.lintcode.com')
		req.add_header('Origin','http://www.lintcode.com')
		req.add_header('Referer','http://www.lintcode.com/zh-cn/accounts/signin/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		codePage = response.read()
		
		code_soup = BeautifulSoup(codePage)
		questionList = code_soup.find_all('p')
		description = '/**\n*' + questionList[1].get_text()
		otherItemList = code_soup.find_all('div',attrs={'class': 'm-t-lg m-b-lg'})
		for otherItem in otherItemList:
			description += otherItem.get_text('*')
		description += '*/\n\n'
		pattern = re.compile('var response =.*?lint_info.*?};')
		codeStrList = re.findall(pattern, codePage)
		codevar =  str(codeStrList[0])
		codeStr = codevar[codevar.find('var response = ') + 15 : - 1]
		codeDict = json.loads(codeStr)

		codeReal = codeDict["solution"]
		
		return description, codeReal

		 
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

	acceptedQuetionList = userSpider.getAcceptedQuetionList(questionPage)

	count = 0

	for acceptedQuetion in acceptedQuetionList:
		count += 1
		submissionId = 	userSpider.getSubmissionId(acceptedQuetion)
		description, myCode = userSpider.getCode(submissionId)
		
		codeFile = open('lintcode/' + acceptedQuetion[9:] + '.cpp', 'w')
		codeFile.write(description)
		codeFile.write(str(myCode).replace('\\n','\n'))
		codeFile.close
		if count % 5 == 0:
			print count


