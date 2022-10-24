from bs4 import BeautifulSoup
from threading import Timer
import time
import requests
import pandas as pd
import json

WooliesProducts = []
pnpProducts = []
MakroProducts = []

baseurlWoolies = 'https://www.woolworths.co.za'
baseurlpnp = 'https://www.pnp.co.za'
baseurlmakro = 'https://www.makro.co.za'

# ------------------ Woolworths Red-Wine Get links

r = requests.get('https://www.woolworths.co.za/cat/WCellar/Wine-Bubbles/Red-Wines/_/N-8slzftZxtznwk?No=0')
soup = BeautifulSoup(r.content, 'lxml')

Wooliesproductlist = soup.find_all('div', class_='product-list__item')

for item in Wooliesproductlist:
    title = item.find('a', {'class': 'range--title'}).text
    price = item.find('strong', {'class': 'price'}).text
    deal = item.find('div', {'class': 'product__special'}).text
    link = item.find('a', {'class': 'product--view'})

    WooliesItems = {
        'Name': title,
        'Price': price,
        'Deal': deal,
        'URL': baseurlWoolies + link['href']
    }
    WooliesProducts.append(WooliesItems)

print('Woolworths Complete!')

# ------------------ Woolworths Red-Wine Get links

r = requests.get('https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?q=%3Arelevance%3AisOnPromotion%3AOn%2BPromotion%3Acategory%3Ared-wine1527159649&pageSize=100')
soup = BeautifulSoup(r.content, 'lxml')

pnpproductlist = soup.find_all('div', class_='productCarouselItemContainer')

for item in pnpproductlist:
    title = item.find('div', {'class': 'item-name'}).text
    currentprice = item.find(
        'div', {'class': 'currentPrice'}).text.strip()[:-2]
    promotion = item.find(
        'div', {'class': 'promotionContainer'}).text.strip()
    link = item.find('a', {'class': 'js-potential-impression-click'})

    pnpItems = {
        'Name': title,
        'Price': currentprice,
        'Deal': promotion,
        'URL': baseurlpnp + link['href']
    }

    pnpProducts.append(pnpItems)

print('PicknPay Complete!')

# ------------------ Makro Red-Wine Get links

r = requests.get(
    'https://www.makro.co.za/beverages-liquor/wines/red-wine/c/JFF?pageSize=80&q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion#')
soup = BeautifulSoup(r.content, 'lxml')

makroproductlist = soup.find_all(
    'div', class_='mak-product-tiles-container__product-tile bv-product-tile mak-product-card-inner-wrapper')

for item in makroproductlist:
    title = item.find('a', {
                        'class': 'product-tile-inner__productTitle js-gtmProductLinkClickEvent text-overflow-ellipsis line-clamp-2'}).text
    price = item.find(
        'p', {'class': 'col-xs-12 price ONPROMOTION'}).text[:-2]
    link = item.find(
        'a', {'class': 'product-tile-inner__img js-gtmProductLinkClickEvent'})

    MakroItems = {
        'Name': title,
        'Price': price,
        'URL': baseurlmakro + link['href']
    }

    MakroProducts.append(MakroItems)

print('Makro Complete!')

# -------- Merging Arrays

combineWine = [*WooliesProducts, *pnpProducts, *MakroProducts]

with open('./public/WineData.json', 'w') as f:
    json.dump(combineWine, f, indent=2)

def stopTheScript():
    exec(open("Scraper.py").read())
    exit()

Timer(43200, stopTheScript).start() #86400 s = 24 h