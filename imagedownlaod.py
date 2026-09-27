
import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def download_images(search_term, number_of_images=5):

    # Chrome settings
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        # Open Google Images
        url = "https://www.google.com/search?tbm=isch&q=" + search_term
        driver.get(url)

        # Give Google time to load images
        time.sleep(3)

        # Find image elements
        images = driver.find_elements(By.CSS_SELECTOR, "img")

        print("Images found:", len(images))

        os.makedirs("downloaded_images", exist_ok=True)

        count = 0

        for image in images:

            if count >= number_of_images:
                break

            image_url = image.get_attribute("src")

            # Ignore Google's small/base64 images
            if not image_url:
                continue

            if not image_url.startswith("http"):
                continue

            try:
                response = requests.get(
                    image_url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    },
                    timeout=10
                )

                if response.status_code == 200:

                    filename = (
                        f"downloaded_images/"
                        f"{search_term}_{count + 1}.jpg"
                    )

                    with open(filename, "wb") as file:
                        file.write(response.content)

                    print("Downloaded:", image_url)
                    print("Saved:", filename)

                    count += 1

            except requests.RequestException:
                continue

        print(f"\nDownloaded {count} images.")

    finally:
        driver.quit()


image_name = input("Enter the image name: ")

download_images(
    image_name,
    number_of_images=5
)
