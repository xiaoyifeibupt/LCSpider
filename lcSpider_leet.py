#! /usr/bin/env python
#coding:utf-8
 
import sys
import os
import re
import urllib2
import urllib
import requests
import cookielib

import getpass

import json

from bs4 import BeautifulSoup

import socket
socket.setdefaulttimeout(100.0) 

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
		
		pattern = re.compile('<input.*?csrfmiddlewaretoken.*?/>')
		item = re.findall(pattern, login_page)
		print 'get csrfmiddlewaretoken success!'
		return item[0][item[0].find('value=') + 7 : -4]
		
 
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
		
		question_soup = BeautifulSoup(problem_page)
		trList = question_soup.find('table', attrs={'id': 'problemList'}).find_all('tr')
		trList.pop(0)
		acceptedQuetionList = []
		for tr in trList:
			if tr.span.attrs['class'][0] == 'ac':
				acceptedQuetionList.append(tr.a.attrs['href'])
		
		print 'getAcceptedQuetionList success'
		return acceptedQuetionList

	def getSubmissionId(self, questionName):
		
		'''download each submission question id'''

		quesURL = domain + questionName + '/submissions/'
		req = urllib2.Request(quesURL)
		req.add_header('Host','leetcode.com')
		req.add_header('Origin','https://leetcode.com')
		req.add_header('Referer','https://leetcode.com/accounts/login/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36')
		response = urllib2.urlopen(req)
		self.operate = self.opener.open(req)
		submissionPage = response.read()
		submission_soup = BeautifulSoup(submissionPage)
		trList = submission_soup.find('table', attrs={'id': 'result_testcases'}).find_all('tr')
		trList.pop(0)
		for tr in trList:
			if tr.find_next('a').find_next('a').string == 'Accepted':
				return tr.find_next('a').find_next('a').attrs['href']

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
		
		code_soup = BeautifulSoup(codePage)
		metaList = code_soup.find('meta', attrs={'name': 'description'})
		metap = re.compile('(\r\n)+')
		subdsc = metap.sub('\n*', str(metaList)[15:-22])
		description = '/**\n*' + subdsc + '\n*/\n'
		
		pattern = re.compile('vm.code.cpp .*?;')
		codeStr = str(re.findall(pattern, codePage)[0])
		codeReal = codeStr[15:-2]
		return description, eval("u'%s'"%codeReal).replace('\r\n','\n')

		 
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage ./lcSpider.py USERNAME'
		sys.exit(0)
	userSpider = xSpider()
	
	username = sys.argv[1]
	password = getpass.getpass('Password:')
	
	userSpider.setLoginInfo(username,password)
	
	csrfmiddlewaretoken = userSpider.preLogin()

	questionPage = userSpider.login(csrfmiddlewaretoken)

	acceptedQuetionList = userSpider.getAcceptedQuetionList(questionPage)
	
	FileExistNames = os.listdir('./leetcode')
	for acceptedQuetion in acceptedQuetionList:
		if acceptedQuetion[10:-1] + '.cpp' not in FileExistNames:
			print 'get ' + acceptedQuetion[10:-1] +'......'
			submissionId = 	userSpider.getSubmissionId(acceptedQuetion)
			description, myCode = userSpider.getCode(submissionId)
			codeFile = open('leetcode/' + acceptedQuetion[10:-1] + '.cpp', 'w')
			codeFile.write(description)
			codeFile.write(myCode)
			codeFile.close
			print 'get ' + acceptedQuetion[10:-1] + '.cpp success'


