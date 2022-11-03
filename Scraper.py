from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from threading import Timer
import time
import requests
import json

driver = Chrome(executable_path='C:\Program Files (x86)\chromedriver')

WooliesProducts = []
pnpProducts = []
MakroProducts = []

baseurlWoolies = 'https://www.woolworths.co.za'
baseurlpnp = 'https://www.pnp.co.za'
baseurlmakro = 'https://www.makro.co.za'

# ------------------ Woolworths Get links

driver.get('https://www.woolworths.co.za/cat/WCellar/Wine-Bubbles/_/N-xtznwkZ1yphczq?No=0&Nrpp=500')

# ---- Page Scroller

total_height = int(driver.execute_script("return document.body.scrollHeight"))

for i in range(1, total_height, 500):
    driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'lxml')

Wooliesproductlist = soup.find_all('div', class_='product-list__item')

for item in Wooliesproductlist:
    title = item.find('a', {'class': 'range--title'}).text
    price = item.find('strong', {'class': 'price'}).text
    deal = item.find('div', {'class': 'product__special'}).text
    link = item.find('a', {'class': 'product--view'})
    img = item.find('img', {'class' :'product-card__img lazyloaded'})


    WooliesItems = {
        'Store': 'WoolWorths',
        'Name': title,
        'Price': price,
        'Deal': deal,
        'URL': baseurlWoolies + link['href'],
        'Image' : img['src']
    }
    WooliesProducts.append(WooliesItems)

print('Woolworths Complete!')


# # ------------------ PicknPay Get links
     
r = requests.get('https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?pageSize=200&q=%3Arelevance%3AisOnPromotion%3AOn%2BPromotion&show=Page#')
soup = BeautifulSoup(r.content, 'lxml')

pnpproductlist = soup.find_all('div', class_='productCarouselItemContainer')

for item in pnpproductlist:
    title = item.find('div', {'class': 'item-name'}).text
    currentprice = item.find('div', {'class': 'currentPrice'}).text.strip()[:-2]
    promotion = item.find('div', {'class': 'promotionContainer'}).text.strip()
    link = item.find('a', {'class': 'js-potential-impression-click'})
    img = item.find('img')

    pnpItems = {
        'Store': 'PicknPay',
        'Name': title,
        'Price': currentprice,
        'Deal': promotion,
        'URL': baseurlpnp + link['href'],
        'Image' : img['src']
    }

    pnpProducts.append(pnpItems)

print('PicknPay Complete!')

# ------------------ Makro Get links

makroWine =[
    'https://www.makro.co.za/beverages-liquor/wines/red-wine/c/JFF?pageSize=80&q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion#',
    'https://www.makro.co.za/beverages-liquor/wines/white-wine/c/JFG?q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion&text=&originalRange=#',
    'https://www.makro.co.za/beverages-liquor/wines/ros-wine/c/JFD?q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion&text=&originalRange=#',
    'https://www.makro.co.za/beverages-liquor/wines/sparkling/c/JFE?q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion&text=&originalRange=#']

for makrowinelinks in range(len(makroWine)):

    driver.get(makroWine[makrowinelinks])

    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    for i in range(1, total_height, 500):
        driver.execute_script("window.scrollTo(0, {});".format(i))
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    makroproductlist = soup.find_all(
        'div', class_='mak-product-tiles-container__product-tile bv-product-tile mak-product-card-inner-wrapper')

    for item in makroproductlist:
        title = item.find('a', {'class': 'product-tile-inner__productTitle js-gtmProductLinkClickEvent text-overflow-ellipsis line-clamp-2'}).text
        price = item.find('p', {'class': 'col-xs-12 price ONPROMOTION'}).text[:-2]
        deal = item.find('div', {'class': 'col-xs-12 saving'}).text[:-2]
        link = item.find('a', {'class': 'product-tile-inner__img js-gtmProductLinkClickEvent'})
        img = item.find('img')
        
        MakroItems = {
            'Store': 'Makro',
            'Name': title,
            'Price': price,
            'Deal': deal,
            'URL': baseurlmakro + link['href'],
            'Image' : img['src']
        }

        MakroProducts.append(MakroItems)

driver.quit()
print('Makro Complete!')

# # -------- Merging Arrays

combineWine = [*WooliesProducts, *pnpProducts, *MakroProducts]

combineWine.sort(key=lambda K: K['Name'])

with open('./public/Data/WineData.json', 'w') as f:
    json.dump(combineWine, f, indent=2,)

print('Complete!')


# def stopTheScript():
#     exec(open("Scraper.py").read())
#     exit()

# Timer(43200, stopTheScript).start() #86400 s = 24 h