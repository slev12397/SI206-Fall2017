import re
from bs4 import BeautifulSoup

opened = open('regex_sum_36399.txt','r').read()
nums = []
# for line in opened.read():
number = re.findall("[0-9]+", opened)
for x in number:
    nums.append(int(x))
print('Sum of Numbers: ' +str(sum(nums)))
print('Amount of Numbers: ' +str(len(nums)))
