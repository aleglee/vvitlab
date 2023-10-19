import requests
from bs4 import BeautifulSoup
import re
import datetime


def week_status():
    url = "https://whataweek.ru"
    req = requests.get(url)
    get = BeautifulSoup(req.text, 'lxml')
    temp = get.find('div', 'uppercase typo-h2')
    temp1 = get.find('div', class_="inline-block leading-none flex-initial mr-8 mb-8").find('span', 'flex-1')
    print(temp1)
    temp2 = re.findall(r'\d+', str(temp1.text))
    week = open('week.txt', 'w')
    week.write(str(temp.text) + '\n' + str(' '.join(map(str, temp2))))



def openfile():
    date = (datetime.datetime.today().strftime("%d/%m/%Y")).split('/')
    file = open('week.txt', 'r')
    week = file.read().splitlines()
    print(week[1].split(' ')[0], date[0], '\n', week[1].split(' ')[1], date[1])
    if week[1].split(' ')[0] <= date[0] or week[1].split(' ')[1] >= date[1]:
        week_status()
        openfile()
    return week
