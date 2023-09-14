import requests
from bs4 import BeautifulSoup
from time import sleep 
import pandas as pd
url = "https://book24.ru/knigi-bestsellery/"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')


link = "https://book24.ru"+soup.find('div', class_='product-list__item').find('a', class_='product-card__name').get('href')
name = soup.find('div', class_='product-list__item').find('a', class_='product-card__name').get('title')
author = soup.find('div', class_='product-list__item').find('div', class_='product-card__authors-holder').text
price = soup.find('div', class_='product-list__item').find('article').get('data-b24-price')


data = []


for p in range(1, 7):
    print(p)
    
    url = f'https://book24.ru/knigi-bestsellery/page-{p}'
    r = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(r.text, 'lxml')


    books = soup.findAll('div', class_='product-list__item')

    for book in books: 
        link = "https://book24.ru"+book.find('a', class_='product-card__name').get('href')
        name = book.find('a', class_='product-card__name').get('title')
        try:
            author = book.find('div', class_='product-card__authors-holder').text
            price = book.find('article').get('data-b24-price')
        except AttributeError:
            author = ' - '
        try:
            full_price = price
            sale = book.find('article').get('data-b24-discount')
            if sale == '0':
                sale = 0 
                full_price = price
            else:
                full_price = int(sale) + int(price)
        except:
            sale = 0
            full_price = price
        data.append([link, name, author, int(price), int(sale), int(full_price)])
    
header = ['Ссылка ', 'Название ', 'Автор ', 'Цена', 'Скидка','Полная стоимость']
df = pd.DataFrame(data, columns=header)
df.to_csv('C:/Users/ryazantsev/Desktop/data.csv', sep=';', encoding='utf-8')
    