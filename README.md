# lcSpider

This script can be used to download all your [LintCode](http://www.lintcode.com/) accepted submissions and questions.

##summary

-	beautifulsoup
-	csrfmiddlewaretoken
-	cookie
-	"\\n" problem




##usage:

	./lcSpider.py USERNAME PASSWORD


##Node:

(1) C++ is the only supported language. But you can easily modify this script to support others.

(2) you may need to install the two libs:[Requests: HTTP for Humans](http://www.python-requests.org/en/latest/ "Requests: HTTP for Humans") and [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/ "Beautiful Soup")

(3) This script will only download the latest successful submission for each problem. If the file exits locally, it will be updated.

##licence

Do What the Fuck You Want to Public License