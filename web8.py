import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

DOWNLOAD_FOLDER = "product_images"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def fetch_page(url):
    """Fetch webpage HTML."""
    try:
        response = requests.get(
            url,
            headers=HEADERS
        )
        response.raise_for_status()
        return response.text

    except requests.RequestException as error:
        print(f"Could not fetch webpage: {error}")
        return None


def extract_title(soup):
    """Extract product title."""
    selectors = [
        "h1",
        "#productTitle",
        ".product-title",
        "[itemprop='name']"
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if element:
            title = element.get_text(" ", strip=True)

            if title:
                return title

    if soup.title:
        return soup.title.get_text(" ", strip=True)

    return "Title not found"


def extract_price(soup):
    """Extract product price."""
    selectors = [
        "[itemprop='price']",
        ".price",
        ".product-price",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".a-price-whole"
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if not element:
            continue

        # Some websites store the price in an attribute.
        raw_price = element.get("content")

        if not raw_price:
            raw_price = element.get_text(" ", strip=True)

        # Remove currency symbols and commas.
        match = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", raw_price)

        if match:
            try:
                return float(match.group().replace(",", ""))
            except ValueError:
                pass

    return None


def extract_image(soup, page_url):
    """Extract product image URL."""
    selectors = [
        "[itemprop='image']",
        "#landingImage",
        "#imgBlkFront",
        ".product-image img",
        ".product-image",
        "img"
    ]

    for selector in selectors:
        image = soup.select_one(selector)

        if not image:
            continue

        image_url = (
            image.get("src")
            or image.get("data-src")
            or image.get("data-original")
        )

        # Handle itemprop=image when it is an <img>.
        if not image_url and image.name == "img":
            image_url = image.get("srcset")

            if image_url:
                image_url = image_url.split(",")[0].strip().split(" ")[0]

        if image_url:
            return urljoin(page_url, image_url)

    return None


def download_image(image_url, product_number):
    """Download product image."""
    if not image_url:
        print("Image URL not found.")
        return None

    try:
        response = requests.get(
            image_url,
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()

        if "png" in content_type:
            extension = ".png"
        elif "webp" in content_type:
            extension = ".webp"
        elif "gif" in content_type:
            extension = ".gif"
        else:
            extension = ".jpg"

        filename = f"product_{product_number}{extension}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"Image downloaded: {filepath}")
        return filepath

    except requests.RequestException as error:
        print(f"Could not download image: {error}")
        return None


def compare_price(price, target_price):
    """Compare current product price with target price."""
    if price is None:
        print("Price could not be extracted.")
        return

    print(f"Current price : ₹{price:,.2f}")
    print(f"Target price  : ₹{target_price:,.2f}")

    if price <= target_price:
        print("RESULT: Product is within your target price.")
    else:
        difference = price - target_price
        print(
            f"RESULT: Product is ₹{difference:,.2f} "
            "above your target price."
        )


def scrape_product(url, target_price, product_number):
    """Fetch and process one product."""
    print("\n" + "=" * 70)
    print(f"PRODUCT {product_number}")
    print("=" * 70)
    print(f"URL: {url}")

    html = fetch_page(url)

    if html is None:
        return

    soup = BeautifulSoup(html, "html.parser")

    title = extract_title(soup)
    price = extract_price(soup)
    image_url = extract_image(soup, url)

    print(f"\nTitle      : {title}")

    if price is not None:
        print(f"Price      : ₹{price:,.2f}")
    else:
        print("Price      : Not found")

    print(f"Image URL  : {image_url or 'Not found'}")

    if image_url:
        download_image(image_url, product_number)

    print("\nPrice comparison:")
    compare_price(price, target_price)


def main():
    print("=" * 70)
    print("              PRODUCT WEB SCRAPER")
    print("=" * 70)

    # Get target price.
    while True:
        try:
            target_price = float(input("\nEnter target price (₹): "))

            if target_price >= 0:
                break

            print("Target price cannot be negative.")

        except ValueError:
            print("Please enter a valid number.")

    # Get number of products.
    while True:
        try:
            product_count = int(
                input("Enter number of product URLs: ")
            )

            if product_count > 0:
                break

            print("Enter a number greater than 0.")

        except ValueError:
            print("Please enter a valid integer.")

    # Get product URLs.
    urls = []

    for i in range(product_count):
        url = input(
            f"Enter product URL {i + 1}: "
        ).strip()

        urls.append(url)

    # Scrape all products.
    for index, url in enumerate(urls, start=1):
        scrape_product(
            url,
            target_price,
            index
        )

    print("\n" + "=" * 70)
    print("SCRAPING COMPLETED")
    print(f"Downloaded images are in: {DOWNLOAD_FOLDER}")
    print("=" * 70)


if __name__ == "__main__":
    main()
