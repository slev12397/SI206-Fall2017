import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
url = 'http://py4e-data.dr-chuck.net/comments_36400.html'
html = urllib.request.urlopen(url).read()

soup = BeautifulSoup(html, 'lxml')
nums = []
for each in soup.find_all('span'):
    nums.append(int(each.text))
print(sum(nums))
