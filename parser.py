import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = ['https://www.kivano.kg/elektronika','https://www.kivano.kg/kompyutery', 'https://www.kivano.kg/bytovaya-tekhnika', 'https://www.kivano.kg/krasota-i-zdorove']

class Parser:
    name = []
    url = []
    categori = []
    def add_ti_list(self):
        for url in urls:
            for i in range(1, 4):
                response = requests.get(f'{url}?page={i}')
                soup = BeautifulSoup(response.text, 'lxml')
                all_items = soup.find_all('div', class_='item product_listbox oh')
                categories = soup.find('div', class_='product-index product-index oh').find('div', class_='portlet-title').find('ul', class_='breadcrumb2').find_all('li')
                cat = categories[1].text.strip()
                
                for j in all_items:
                    item = j.find('strong').text.strip()
                    href =  j.find('a').get('href')
                    
                    self.name.append(item)
                    self.url.append(href)
                    self.categori.append(cat)

class Writer:
    def __init__(self, a):
        self.a = a
        self.kivanoDF = pd.DataFrame(
            {
             'name':a.name,
             'url':a.url,
             'categori':a.categori
            }
        )
    def write_to_csv(self):
        csvFileContents = self.kivanoDF.to_csv(index=False)
        with open('kivano.csv', 'w', encoding='utf-8') as f:
            f.write(csvFileContents)

p = Parser()
p.add_ti_list()
w = Writer(p)
w.write_to_csv()