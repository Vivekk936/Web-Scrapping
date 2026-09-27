import os

import requests
import re

user = input("Enter the image name: ")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"

    )
}

url=f"https://www.google.com/search?sca_esv=81be1d65d23458ac&rlz=1C1PNFE_enIN1183IN1183&sxsrf=APpeQntuiZnYhinyj-bs33qi_4noNDRAdw:1790430789078&udm=2&fbs=ABfTbFVyMZGZf1hfvX9uKjN_-G8c4u0nXx4bEIpwm1lnNH832VstEKsVDqPorK0Gahnm2nq-aQnTz_mBV-EZYISbLc-StUIq_PhL7hb0Qt0YiIGOHkJjnTZ-cOFt4MBdBh9xxUSLmQqYmceNOVPnJ828B2jVF7369v0TJ7PslRO7NeHq_gersSL0dF9_aQb9YBem2DXpczx9t0eeLk_LAjFQmfrB7VpT0w&q={user}&sa=X&ved=2ahUKEwjY3bW5soyXAxUVmuEIHR3MMS0QtKgLegQIHhAB&biw=1440&bih=765&dpr=1"

response = requests.get(
    url=url,
    headers=headers
).content

pattern=r"https://support\.google\.com/websearch"

links = re.findall(pattern , response)
print("\nFound links:\n")
print("Total Images Found:",len(links))
no_of_images=int(input("Enter the no. of images you want to download: "))

if links:
    if not os.path.exists(user):
        os.makedirs(user)
        os.chdir(user)

    else:
        os.chdir(user)

    for link in links[:no_of_images]:
        image_url=link
        response=requests.get(url=image_url).content
        image_name=image_url.split("/")[-1]
        with open(image_name,"wb") as f:
            f.write(response)



