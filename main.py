import requests
from bs4 import BeautifulSoup
import lxml
import sqlite3 as sql

querry_add_product = '''INSERT INTO products (name, sku, price) VALUES (?,?, ?)'''
def parser(url):
    try:
        with sql.connect('products.db') as conn:
            list_products = []
            url = 'https://glavsnab.net/tovary-dlya-doma/mebel/krovati.html?limit=100'
            res = requests.get(url)
            soup = BeautifulSoup(res.text,'lxml')
            products = soup.find_all('div',class_ = 'product-card')
            for product in products:
                name  = product.get('data-product-name')
                sku = product.find('span',class_ = 'product-card__key').text
                price = product.find('span',itemprop = 'price').text
                res = (name,sku,price)
                print(res)
                list_products.append(res)
            for row in list_products:
                conn.cursor().execute(querry_add_product,(row[0],row[1],row[2]))
            
        
                
            
           
    except sql.IntegrityError:
        return 'Error'
    except sql.OperationalError:
        return 'Error'



if __name__ == '__main__':
    parser(url = 'https://glavsnab.net/tovary-dlya-doma/mebel/krovati.html?limit=100')
    

