import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

# PART A
url = 'http://py4e-data.dr-chuck.net/comments_36400.html'
html = urllib.request.urlopen(url).read()

soup = BeautifulSoup(html, 'lxml')
nums = []
for each in soup.find_all('span'):
    nums.append(int(each.text))
print(sum(nums))

# PART B
def follow(a,b):
    name=[]
    url = 'http://py4e-data.dr-chuck.net/known_by_Marty.html'
    for x in range(a):
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
        q = soup.find_all('a')
        pick = q[(b-1)]
        url = pick['href']
        name.append(pick.text)
    print(name[-1])

follow(7,18)
