import requests
from bs4 import BeautifulSoup as soup
import json, os

drivers_path = os.path.join(os.getcwd() + '/chromedriverpath/chromedriver_win32/chromedriver.exe')

print(drivers_path)
import sys

sys.exit()

def search_product():

  main_url = 'https://hasbropulse.com/collections/new/products.json'
  r = requests.get(main_url)

  products = r.json()['products']
  
  for product in products:
    # print(product['title'])
    if c['keywords'] in product['title']:
      print('Product found!!')
      # print(product['title'])

      # Returns the variantId used for adding a product to cart
      return product['variants'][0]['id']


def main():

  print('Searching for ' + c['keywords'])

  variant_id = search_product()

  add_to_cart = 'https://hasbropulse.com/cart/' + str(variant_id) + ':1'

  r = requests.post(add_to_cart)

  if 'stock_problems' in r.url:
    print('Product is Sold-Out!!')
  elif 'cart' in r.url:
    print('Carting was unsuccessful, or product no longer available')
  else:
    print('Checkout link: ' + r.url)

if __name__ == '__main__':

  try:
    with open('config.json') as json_data:
      c = json.load(json_data)

    main()

  except FileNotFoundError:
    print('config.json file does not exist')