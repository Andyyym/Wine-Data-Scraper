from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import json

PnPbaseurl = 'https://www.pnp.co.za'
Makrobaseurl = 'https://www.makro.co.za'
Wooliesbaseurl = 'https://www.woolworths.co.za'

productlinksPnP = []
productlinksMakro = []
productlinksWoolies = []


# ------------------ Woolworths Red-Wine Get links

WooliesWineList = []
wooliesred = 'https://www.woolworths.co.za/cat/WCellar/Wine-Bubbles/Red-Wines/_/N-8slzftZxtznwk?No=0'
woolieswhite = 'https://www.woolworths.co.za/cat/White-Wines/_/N-ni26q6Zxtznwk?No=0'

r = requests.get(wooliesred)
soup = BeautifulSoup(r.content, 'lxml')


Wooliesproductlist = soup.find_all('div', class_='product-list__item')

for item in Wooliesproductlist:
    for link in item.find_all('a', class_='product--view', href=True):
        productlinksWoolies.append(Wooliesbaseurl + link['href'])

print('Waiting: 5 seconds')
time.sleep(5)

#-------WHITE-------------

r = requests.get(woolieswhite)
soup = BeautifulSoup(r.content, 'lxml')


Wooliesproductlist = soup.find_all('div', class_='product-list__item')

for item in Wooliesproductlist:
    for link in item.find_all('a', class_='product--view', href=True):
        productlinksWoolies.append(Wooliesbaseurl + link['href'])

# ------------------ Makro Red-Wine Get links

MakroWineList = []
makrored = 'https://www.makro.co.za/beverages-liquor/wines/red-wine/c/JFF?q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion&text=&originalRange=100#'
makrowhite = 'https://www.makro.co.za/beverages-liquor/wines/white-wine/c/JFG?q=%3Arelevance%3AsashOverlayTitle%3AOn%2BPromotion&text=&originalRange=100#'

r = requests.get(makrored)
soup = BeautifulSoup(r.content, 'lxml')

Makroproductlist = soup.find_all(
    'div', class_='mak-product-tiles-container__product-tile bv-product-tile mak-product-card-inner-wrapper')

for item in Makroproductlist:
    for sale in item.find_all('span', class_='ONPROMOTION'):
        for link in item.find_all('a', class_='product-tile-inner__img js-gtmProductLinkClickEvent', href=True):
            productlinksMakro.append(Makrobaseurl + link['href'])

print('Waiting: 5 seconds')
time.sleep(5)

#-------WHITE-------------

r = requests.get(makrowhite)
soup = BeautifulSoup(r.content, 'lxml')

Makroproductlist = soup.find_all(
    'div', class_='mak-product-tiles-container__product-tile bv-product-tile mak-product-card-inner-wrapper')

for item in Makroproductlist:
    for sale in item.find_all('span', class_='ONPROMOTION'):
        for link in item.find_all('a', class_='product-tile-inner__img js-gtmProductLinkClickEvent', href=True):
            productlinksMakro.append(Makrobaseurl + link['href'])



# ---------------------- Pick n Pay Red-Wine Get Links

PicknPayWineList = []

pnpred = 'https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?q=%3Arelevance%3AisOnPromotion%3AOn%2BPromotion%3Acategory%3Ared-wine1527159649&pageSize=100'
pnpwhite = 'https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?q=%3Arelevance%3Acategory%3Awhite-wine1527159649%3AisOnPromotion%3AOn%2BPromotion&text=&pageSize=100#'

r = requests.get(pnpred)
soup = BeautifulSoup(r.content, 'lxml')

PnPproductlist = soup.find_all('div', class_='productCarouselItemContainer')

for item in PnPproductlist:
    for link in item.find_all('a', class_='js-potential-impression-click', href=True):
        productlinksPnP.append(PnPbaseurl + link['href'])

print('Waiting: 5 seconds')
time.sleep(5)

#-------WHITE-------------

r = requests.get(pnpwhite)
soup = BeautifulSoup(r.content, 'lxml')

PnPproductlist = soup.find_all('div', class_='productCarouselItemContainer')

for item in PnPproductlist:
    for link in item.find_all('a', class_='js-potential-impression-click', href=True):
        productlinksPnP.append(PnPbaseurl + link['href'])


#-----Formnat to JSON

for link in productlinksPnP:  
    PnP = { 
        'Link': link
    }

    PicknPayWineList.append(PnP)

for link in productlinksMakro:  
    Makro = { 
        'Link': link
    }

    MakroWineList.append(Makro)

for link in productlinksWoolies:  
    Woolworths = { 
        'Link': link
    }

    WooliesWineList.append(Woolworths)


# --------Loading Data to JSON Makro


with open('./Data/Makro.json', 'w') as f:
    print('Saving: Makro Data')
    json.dump(MakroWineList, f, indent=2)


# --------Loading Data to JSON PnP

with open('./Data/PicknPay.json', 'w') as f:
    print('Saving: PicknPay Data')
    json.dump(PicknPayWineList, f, indent=2)


# --------Loading Data to JSON PnP

with open('./Data/Woolworths.json', 'w') as f:
    print('Saving: WoolWorths Data')
    json.dump(WooliesWineList, f, indent=2)


# -------- Merging Arrays

combineWine = [*PicknPayWineList, *MakroWineList, *WooliesWineList]

with open('./Data/RedWine.json', 'w') as f:
    print('Merging Data. . .')
    json.dump(combineWine, f, indent=2)

print("Complete")