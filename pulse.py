import requests
from bs4 import BeautifulSoup as soup
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import webbrowser

if os.name == 'nt':
  driver_path = os.path.join(os.getcwd() + '/chromedriverpath/chromedriver_win32/chromedriver.exe')
elif os.name == 'darwin':
  driver_path = os.path.join(os.getcwd() + '/chromedriverpath/chromedriver_mac64/chromedriver')

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options, executable_path=(driver_path))

def search_product():

  main_url = 'https://hasbropulse.com/collections/new/products.json'

  r = requests.get(main_url)

  products = r.json()['products']
  
  for product in products:
    # print(product['title'])
    if c['keyword'] in product['title']:
      print('Product found!!')
      # print(product['title'])

      # Returns the variantId used for adding a product to cart
      return product['variants'][0]['id']


def main():

  print('Searching for ' + c['keyword'])

  variant_id = search_product()

  add_to_cart = 'https://hasbropulse.com/cart/' + str(variant_id) + ':1'

  r = requests.post(add_to_cart)

  if 'stock_problems' in r.url:
    print('Product is Sold-Out!!')
  elif 'cart' in r.url:
    print('Carting was unsuccessful, or product no longer available')
  else:
    print('Checkout link: ' + r.url)
    webbrowser.open_new(r.url)

    driver.get(r.url)

    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary']")))

if __name__ == '__main__':

  try:
    with open('config.json') as json_data:
      c = json.load(json_data)

    main()

  except FileNotFoundError:
    print('config.json file does not exist')