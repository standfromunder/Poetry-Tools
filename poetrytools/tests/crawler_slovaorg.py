import requests
from bs4 import BeautifulSoup
import re
import os
import shutil
import json
import sqlite3
# """
# url = 'https://slova.org.ru/'
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# links_periods = []
# for period in soup.find_all('a', href = True):
#     links_periods.extend(re.findall(r'/\w+-\w+/', str(period)))
# print(links_periods)

main_link = 'https://slova.org.ru/'
url_gold = 'https://slova.org.ru/zolotoj-vek/'
url_silv = 'https://slova.org.ru/serebryanyj-vek/'
url_sov = 'https://slova.org.ru/sovetskij-period/'
ASSETS_PATH = 'C:\python\Poetry-Tools\poetrytools\poems'

links_periods = [url_gold, url_silv, url_sov]
tags = ['grid-col-1', 'grid-221 grid-gap-xl', '', '']
authors = {}


try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    sqlite_connection.commit()




except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
# finally:
#     if (sqlite_connection):
#         sqlite_connection.close()
#         print("Соединение с SQLite закрыто")


for i in range(len(links_periods)):
    r = requests.get(links_periods[i])
    soup = BeautifulSoup(r.text, 'html.parser')
    period = soup.find('h3').text
    for many_authors in soup.find_all('div', class_='grid-221 grid-gap-xl'):
        for author in many_authors.find_all('a'):
            if period not in authors:
                authors[period] = []
            authors[period].append({author.text: (re.findall(r'/[\w-]+/', str(author)))[0]})

print(authors)
links_poems = {}
id = 0
for period, authors_1 in authors.items():
    for one_author in authors_1:
        for name, link in one_author.items():
            r = requests.get(main_link+link)
            soup = BeautifulSoup(r.text, 'html.parser')
            poems = soup.find('div', class_='grid-532 grid-gap-l').find_all('a')
            for poem in poems:
                if poem.text == 'Биография' or poem.text == 'Лучшие стихотворения': continue
                poem_link = re.findall(r'/\w+/[\w-]+/', str(poem))
                if poem_link :
                    r = requests.get(main_link + poem_link[0])
                    soup = BeautifulSoup(r.text, 'html.parser')
                    if period != 'Серебряный век' or '<pre>' not in soup.prettify():
                        poems = soup.find('div', class_='grid-532 grid-gap-l').find_all('p', class_=None)
                    else:
                        poems = soup.find('div', class_='grid-532 grid-gap-l').find_all('pre')

                    final_poem = ''
                    for abz in poems:
                        final_poem += (str(abz).replace('<br/>','\n')).replace('</p>', '\n\n').replace('<p>','').replace('<pre>', '').replace('</pre>', '')
                    nottext = re.findall(r'<em>[\s\S]+?<\/em>', final_poem)
                    for i in nottext:
                        final_poem = final_poem.replace(i, '')
                    nottext = re.findall(r'<strong>[\s\S]+?<\/strong>', final_poem)
                    for i in nottext:
                        final_poem = final_poem.replace(i, '')
                    final_poem = final_poem.strip()
                    print(final_poem)
                    if final_poem == '': continue
                    id += 1
                    cursor.execute('''INSERT INTO poems VALUES
                                     (?, ?, ?, ?, ?);''',(id, period, name, poem.text, final_poem))
                    sqlite_connection.commit()

print(links_poems)


