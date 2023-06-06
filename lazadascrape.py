from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
chrome_options = Options()
chrome_options.add_argument("--headless")

driver_path = './chromedriver.exe'

browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

def scrapeLazada(query) -> list[dict]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver_path = './chromedriver.exe'

    browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    search_url = f'https://www.lazada.co.id/catalog/?q={query}&_keyori=ss'

    # load the search page
    browser.get(search_url)
    browser.execute_script("window.scrollTo(300, 0);")
    scroll_height = browser.execute_script("return document.body.scrollHeight")
    while browser.execute_script("return window.pageYOffset + window.innerHeight") < scroll_height:
        browser.execute_script("window.scrollBy(0, 50);")
        time.sleep(0.1)

    html_content = browser.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    product_items = soup.find_all('div', {'class': 'Bm3ON'})
    products = []
    #print(product_items)

    for product_item in product_items:
        #print(product_item)
        img = product_item.find('img',{'class':'jBwCF'})['src']
        name = product_item.find('img',{'class':'jBwCF'})['alt']
        link = product_item.find('a')['href']
        # link = link.replace("//", "")
        price = product_item.find('span', {'class': 'ooOxS'}).text

        products.append({'linke': link,'img_srce': img,'namee':name, 'pricee': price})
    return products
