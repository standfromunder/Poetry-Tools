import requests
from bs4 import BeautifulSoup
import re
import os
import shutil
import json
import sqlite3

main_link = 'https://stihi.ru/rating.html?'
base_link = 'https://stihi.ru'

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    # sqlite_connection.commit()





except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

cursor.execute('SELECT poem from poems where author = "Людмила Абсатарова"')
records = cursor.fetchall()
print(records)
'''
download from stihi.ru
'''
# id = 16600
# for page in range(1,4):
#     if id > 22133: break
#     r = requests.get(main_link+str(page))
#     soup = BeautifulSoup(r.text, 'html.parser')
#     for author_link in soup.find_all('a', class_='recomlink'):
#         link = author_link.get('href')
#         links = [link, link+'&s=50']
#         print(links)
#         for link in links:
#             r = requests.get(base_link+link)
#             soup = BeautifulSoup(r.text, 'html.parser')
#             for poem in soup.find_all('a', class_='poemlink'):
#                 id += 1
#                 r = requests.get(base_link + poem.get('href'))
#                 soup = BeautifulSoup(r.text, 'html.parser')
#                 title = soup.find('h1').text
#                 text = soup.find('div', class_='text')
#                 if text:
#                     text = text.text
#                     for nottext in re.findall(r'[А-я|\s]+:\nhttp.+', text):
#                         text = text.replace(nottext, '')
#                     text = text.replace('vng.', '')
#                     text = text.strip()
#                     print(id, author_link.text, title, text)
#                     # cursor.execute('''INSERT INTO poems VALUES
#                     #                                      (?, ?, ?, ?, ?);''', (id, 'Современная поэзия', author_link.text, title, text))
#                     # sqlite_connection.commit()

if sqlite_connection:
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")