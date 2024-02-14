import requests
import json
import time

class PnPWebScraper:
   def __init__(self):
      self.base_url = "https://www.pnp.co.za/pnphybris/v2/pnp-spa/products/search"
      self.params = {
         "fields": "products(sponsoredProduct,code,name,averageWeight,summary,price(FULL),images(DEFAULT),stock(FULL),averageRating,numberOfReviews,variantOptions,maxOrderQuantity,productDisplayBadges(DEFAULT),allowedQuantities(DEFAULT),available,defaultQuantityOfUom,inStockIndicator,defaultUnitOfMeasure,potentialPromotions(FULL),categoryNames)",
         "query": ":relevance:allCategories:wine800952112",
         "pageSize": 100,
         "storeCode": "WC44",
         "lang": "en",
         "curr": "ZAR"
      }
      self.pnpProducts = []

   def scrape(self):
      page = 0
      while True:
         self.params["currentPage"] = page
         try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])

            if not products:
               break

            for product in products:
               name = product.get("name")
               formatted_value = product.get("price", {}).get("formattedValue")
               primary_image = next((image.get("url") for image in product.get("images", []) if image.get("format") == "product"), None)
               potential_promotions = product.get("potentialPromotions", [])
               instock = product.get("stock", {}).get("stockLevelStatus")
               promotion_message = next((promotion.get("promotionTextMessage") for promotion in potential_promotions), None)
               promotion_end_date = next((promotion.get("endDate") for promotion in potential_promotions), None)

               pnpItems = {
                  'StoreName': 'PicknPay',
                  'ItemName': name,
                  'Price': formatted_value,
                  'Image': primary_image,
                  'PromotionMessage': promotion_message,
                  'OnPromotion': bool(promotion_message),
                  'PromotionEndDate': promotion_end_date,
                  "Stock": instock
               }
               self.pnpProducts.append(pnpItems)

            page += 1
            time.sleep(3)
         except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

      self.pnpProducts.sort(key=lambda K: K['ItemName'])

   def save_to_json(self, filename):
      try:
         with open(filename, 'w') as f:
            json.dump(self.pnpProducts, f, indent=2)
      except IOError as e:
         print(f"An error occurred while saving to JSON: {e}")

   def get_product_count(self):
      return len(self.pnpProducts)


scraper = PnPWebScraper()
scraper.scrape()
scraper.save_to_json('WineData.json')
product_count = scraper.get_product_count()
print(f"Number of products found: {product_count}")
