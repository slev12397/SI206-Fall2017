import re

opened = open('mbox-short.txt', 'r')
read = opened.readlines()
lst =[]
for line in read:
    x = re.findall('^X-DSPAM-Confidence: ([0-9.]+)', line)
    if len(x) > 0:
        print(x)
for line in read:


    name = re.findall('(\S+)@',line)
    if len(name) > 0:
        print(name)
