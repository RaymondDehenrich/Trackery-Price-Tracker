from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

chrome_options = Options()
chrome_options.add_argument("--headless")

driver_path = './chromedriver.exe'
browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

def scrapeLazada(query) -> list[dict]:
    url = f"https://www.lazada.co.id/tag/{query}/?ajax=true&isFirstRequest=true&page=1"
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    try:
        data = json.loads(soup.find("body").text)
        items = data["mods"]["listItems"]

        parsed_items = []

        for item in items:
            parsed_items.append(
            {
                'link': item["itemUrl"],
                'img_src': item["image"],
                'name': item["name"],
                'price': item["priceShow"]
            })

        return parsed_items
    except:
        return []
