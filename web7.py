import re
import os
import requests
from bs4 import BeautifulSoup




class PriceTracer:
    def __init__(self,url):
        self.url = url
        self.user_agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36'}
        self.response = requests.get(url=self.url,headers=self.user_agent).text
        self.soup = BeautifulSoup(self.response,"lxml")
    def product_title(self):
        title=self.soup.find("span",{"id":"productTitle"})
        if title is not None:
            return title.text.strip()
        else:
            return "None"
    def product_price(self):
        price=self.soup.find("span",{"class":"a-price-whole"})
        if price is not None:
            price=price.text.strip()
            price = price.replace(",", "").replace(".", "")
            return int(price)
        else:
            return "None"""

    def get_product_image(self):
        image = self.soup.find("img",id="landingImage")

        if image:
            image_url=image.get("src")
            print(image_url)
            image_response=requests.get(image_url,headers=self.user_agent)
            if image_url:
                os.makedirs("images")
                os.chdir("images")
            else:
                os.chdir("images")
            with open("Product.jpg","wb") as code:
                code.write(image_response.content)
            print("Image saved")
        else:
            return "None"

        return None




device=PriceTracer(input("enter the url"))
target=int(input("Enter the Target Price"))
print("Product title:",device.product_title())
print("Product Price:",device.product_price())
device.get_product_image()
if device.product_price()>target:
    print("The price is greater than the target by:",(int(device.product_price())-target))
else:
    print("The price is less than the target by:",(target-int(device.product_price())))
