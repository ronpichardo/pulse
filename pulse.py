import requests
from bs4 import BeautifulSoup as soup
import json, os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if os.name == 'nt':
  driver_path = os.path.join(os.getcwd() + '/chromedriverpath/chromedriver_win32/chromedriver.exe')
elif os.name == 'darwin':
  driver_path = os.path.join(os.getcwd() + '/chromedriverpath/chromedriver_mac64/chromedriver')

chrome_options = Options()
chrome_options.add_argument('--incognito')
# chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options, executable_path=(driver_path))

def search_product():

  main_url = 'https://hasbropulse.com/collections/new/products.json'

  r = requests.get(main_url)

  if 'password' in r.url:
    print('New products to drop soon...')
    time.sleep(2)
    search_product()
  else:
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

  try:

    add_to_cart = 'https://hasbropulse.com/cart/' + str(variant_id) + ':1'

    r = requests.post(add_to_cart)

    if 'stock_problems' in r.url:
      print('Product is Sold-Out!!')
    elif 'cart' in r.url:
      print('Carting was unsuccessful, or product no longer available')
    else:
      print('Checkout link: ' + r.url)
      # webbrowser.open_new(r.url)

      print('Inputing User Info')
      driver.get(r.url)

      # Finding Shipping details to submit

      email_addr = driver.find_element_by_id('checkout_email')
      first_name = driver.find_element_by_id('checkout_shipping_address_first_name')
      last_name = driver.find_element_by_id('checkout_shipping_address_last_name')
      street_addr = driver.find_element_by_id('checkout_shipping_address_address1')
      city = driver.find_element_by_id('checkout_shipping_address_city')
      zip_code = driver.find_element_by_id('checkout_shipping_address_zip')
      state = Select(driver.find_element_by_id('checkout_shipping_address_province'))
      phone_num = driver.find_element_by_id('checkout_shipping_address_phone')
      
      # Finds the continue to shipping button
      continue_to_shipping = driver.find_element_by_id('continue_button')

      # Inputs the user shipping details from the config file
      email_addr.send_keys(c['shipping']['email'])
      first_name.send_keys(c['shipping']['first'])
      last_name.send_keys(c['shipping']['last'])
      street_addr.send_keys(c['shipping']['address'])
      city.send_keys(c['shipping']['city'])
      state.select_by_value(c['shipping']['state'])
      zip_code.send_keys(c['shipping']['zip'])
      phone_num.send_keys(c['shipping']['phone'])

      # Click the continue to shipping button after user data has been input
      continue_to_shipping.click()

      # Waits 1 second for the page to load
      # ** Future implementation will be with WebDriverWait Method **
      time.sleep(1)

      # Shipping details are usually pre-filled in, determined from shipping address
      # from previous inputs

      # After page loads, find the continue button and click it
      continue_to_payment = driver.find_element_by_id('continue_button')
      continue_to_payment.click()

      # Wait 2 seconds for the page to load...takes longer than the  previous steps to load

      # Manually input user credit card details...xpaths are in an iframe which is not as 
      # simple to parse, ** WiP to implement **


      # wait = WebDriverWait(driver, 10)
      # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary']")))

  except Exception as e:
    print('Exception thrown!: %s' % e)

if __name__ == '__main__':

  try:
    with open('config.json') as json_data:
      c = json.load(json_data)

    main()

  except FileNotFoundError:
    print('config.json file does not exist')