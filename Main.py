import json
import time
import os
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from apscheduler.schedulers.blocking import BlockingScheduler

# Store URL details
URL_DETAILS = [
    {
        'store': 'WoolWorths',
        'base_url': 'https://www.woolworths.co.za',
        'scraper': 'woolworth_scraper',
        'url': 'https://www.woolworths.co.za/cat/WCellar/Wine-Bubbles/_/N-xtznwkZ1yphczq?No=0&Nrpp=500'
    },
    {
        'store': 'PicknPay',
        'base_url': 'https://www.pnp.co.za',
        'scraper': 'pnp_scraper',
        'url': 'https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?pageSize=200&q=%3Arelevance%3AisOnPromotion%3AOn%2BPromotion&show=Page#'
    },
    # Other stores...
]


def get_last_scrape_time():
    if not os.path.exists('last_scrape_time.json'):
        return None
    with open('last_scrape_time.json', 'r') as f:
        timestamp = json.load(f)
    return datetime.datetime.fromisoformat(timestamp)


def set_last_scrape_time(time):
    with open('last_scrape_time.json', 'w') as f:
        json.dump(time.isoformat(), f)


def pnp_scraper(base_url):
    pnpProducts = []
    r = requests.get(
        'https://www.pnp.co.za/pnpstorefront/pnp/en/All-Products/Wine/c/wine-423144840?pageSize=200&q=%3Arelevance%3AisOnPromotion%3AOn%2BPromotion&show=Page#')
    soup = BeautifulSoup(r.content, 'lxml')

    pnpproductlist = soup.find_all(
        'div', class_='productCarouselItemContainer')

    for item in pnpproductlist:
        title = item.find('div', {'class': 'item-name'}).text
        currentprice = item.find('div', {'class': 'currentPrice'}).text.strip()
        promotion = item.find(
            'div', {'class': 'promotionContainer'}).text.strip()
        link = item.find('a', {'class': 'js-potential-impression-click'})
        img = item.find('img')

        pnpItems = {
            'Store': 'PicknPay',
            'Name': title,
            'Price': currentprice,
            'Deal': promotion,
            'URL': base_url + link['href'],
            'Image': img['src']
        }

        pnpProducts.append(pnpItems)

    return pnpProducts


def init_webdriver():
    # Set up webdriver options
    webdriver_service = Service('C:\Program Files (x86)\chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    return driver


def woolworth_scraper(driver, base_url):
    products = []

    driver.get(
        'https://www.woolworths.co.za/cat/WCellar/Wine-Bubbles/_/N-xtznwkZ1yphczq?No=0&Nrpp=500')

    # Scroll the page
    total_height = int(driver.execute_script(
        "return document.body.scrollHeight"))
    for i in range(1, total_height, 500):
        driver.execute_script("window.scrollTo(0, {});".format(i))
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    product_list = soup.find_all('div', class_='product-list__item')
    for item in product_list:
        # Extract details and append to list
        # Similar error handling can be added here
        title = item.find('a', {'class': 'range--title'}).text
        price = item.find('strong', {'class': 'price'}).text
        deal = item.find('div', {'class': 'product__special'}).text
        link = item.find('a', {'class': 'product--view'})
        img = item.find('img', {'class': 'product-card__img lazyloaded'})

        item_details = {
            'Store': 'WoolWorths',
            'Name': title,
            'Price': price,
            'Deal': deal,
            'URL': base_url + link['href'],
            'Image': img['src']
        }
        products.append(item_details)

    return products

def main():
    driver = init_webdriver()

    all_products = []
    for url_detail in URL_DETAILS:
        if url_detail['scraper'] == 'woolworth_scraper':
            all_products += woolworth_scraper(driver, url_detail['base_url'])
        elif url_detail['scraper'] == 'pnp_scraper':
            all_products += pnp_scraper(url_detail['base_url'])

    driver.quit()

    # Sort and write to file
    all_products.sort(key=lambda K: K['Name'])
    with open('./Data/WineData.json', 'w') as f:
        json.dump(all_products, f, indent=2)

    print('Complete!')

scheduler = BlockingScheduler()

# Schedule the function to run every 12 hours
scheduler.add_job(main, 'interval', hours=6)

# Start the scheduler
scheduler.start()

if __name__ == "__main__":
    main()
