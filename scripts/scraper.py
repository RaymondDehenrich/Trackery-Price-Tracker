import requests
from bs4 import BeautifulSoup

def scrapeTokopedia(name):
    url = 'https://www.tokopedia.com/search?st=product&q='+name
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Language": "en-US,en;q=0.9" 
}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_divs = soup.find_all('div', {'id': 'spnSRPProdPrice'})
    #ini hanya dapet price, blm dapet nama, gambar(kalo perlu)

def scrapeShopee(name):
    url = 'https://shopee.co.id/search?keyword='+name
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Language": "en-US,en;q=0.9" 
}
    response = requests.get(url,headers=headers)
    return

def scrapeLazada(name):
    url = f'https://www.lazada.co.id/catalog/?q={name}&_keyori=ss'
    headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Language": "en-US,en;q=0.9" 
}
    response = requests.get(url,headers=headers)
    return



def dailyScrape():
    #Code here for getting data from the database, should be in a form of 1d array with inside of it is name

    #end code
    #Node: Name need to be pre-processed so that any space ' ' changed into '+', atleast on tokopedia. other idk
    scrapelist =['bakso','kalkulator']#temp array
    for i in scrapelist:
        scrapeLazada(i)
        scrapeShopee(i)
        scrapeTokopedia(i)
    return


dailyScrape()