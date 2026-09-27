# 🕷️ Web Scraping & Price Tracker

A Python-based web scraping project that extracts product information from webpages using **Requests** and **BeautifulSoup**.

The project can retrieve product titles, prices, and images, download product images, and compare the current product price with a user-defined target price.

---

## 🚀 Features

* 🌐 Scrape product webpages
* 🔎 Extract product titles
* 💰 Extract and process product prices
* 🖼️ Extract product image URLs
* 📥 Download product images automatically
* 🎯 Compare product prices with a target price
* 📊 Calculate the difference between current and target prices
* 🧹 Clean scraped price data for numerical comparison
* 🐍 Built with Python
* 📄 Parse HTML using BeautifulSoup

---

## 🛠️ Technologies Used

* **Python**
* **Requests** – for sending HTTP requests
* **BeautifulSoup** – for parsing HTML
* **lxml** – HTML parser
* **Regular Expressions** – for extracting and processing data

---

## 📂 Project Structure

```text
web-scrapping/
│
├── web.py
├── web5.py
├── web6.py
├── web7.py
├── Product.jpg
├── README.md
└── .venv/
```

> `.venv/` is the Python virtual environment and normally should not be uploaded to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd web-scrapping
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install requests beautifulsoup4 lxml
```

---

## ▶️ Running the Project

Run the main scraper:

```bash
python web7.py
```

The program will ask for:

```text
Enter the URL:
Enter the Target Price:
```

For example:

```text
Enter the URL: https://www.amazon.in/...
Enter the Target Price: 180000
```

The program then extracts the product information.

---

## 📊 Example Output

```text
Product title: iPhone 18 Pro (256 GB) - Silver
Product Price: 164900
Image URL: https://m.media-amazon.com/images/I/71E-J09sb6L._SL1500_.jpg
Image saved successfully!

The price is less than the target by: 15100
```

---

## 🔍 How It Works

The scraper follows this basic workflow:

```text
          Product URL
               │
               ▼
       Send HTTP Request
               │
               ▼
        Receive HTML
               │
               ▼
      BeautifulSoup Parser
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
     Title   Price    Image
       │       │        │
       │       │        ▼
       │       │   Download Image
       │       │
       └───────┼────────┘
               ▼
       Compare Price
               │
               ▼
        Display Result
```

---

## 💰 Price Tracking

The project accepts a target price from the user.

For example:

```text
Current Price = ₹164,900
Target Price  = ₹180,000
```

The program calculates:

```text
180000 - 164900 = 15100
```

Output:

```text
The price is less than the target by: 15100
```

If the current price is greater than the target price, the program calculates how much higher it is.

---

## 🖼️ Image Downloading

The scraper searches for the product's main image:

```python
image = self.soup.find("img", id="landingImage")
```

It then retrieves the image URL:

```python
image_url = image.get("data-old-hires") or image.get("src")
```

Finally, the image is downloaded using:

```python
image_response = requests.get(image_url)

with open("Product.jpg", "wb") as file:
    file.write(image_response.content)
```

The downloaded image is saved as:

```text
Product.jpg
```

---

## 🧹 Price Cleaning

Websites may return prices in formats such as:

```text
1,64,900.
```

The scraper removes commas and periods:

```python
price = price.replace(",", "").replace(".", "")
```

The result becomes:

```text
164900
```

which can then be converted into an integer:

```python
return int(price)
```

---

## 🧑‍💻 Example Code

A simplified version of the scraper:

```python
import requests
from bs4 import BeautifulSoup


class PriceTracer:

    def __init__(self, url):
        self.url = url

        self.user_agent = {
            "User-Agent": "Mozilla/5.0"
        }

        self.response = requests.get(
            url=self.url,
            headers=self.user_agent
        ).text

        self.soup = BeautifulSoup(
            self.response,
            "lxml"
        )

    def product_title(self):

        title = self.soup.find(
            "span",
            {"id": "productTitle"}
        )

        if title:
            return title.text.strip()

        return "None"

    def product_price(self):

        price = self.soup.find(
            "span",
            {"class": "a-price-whole"}
        )

        if price:
            price = price.text.strip()
            price = price.replace(",", "").replace(".", "")
            return int(price)

        return 0

    def get_product_image(self):

        image = self.soup.find(
            "img",
            id="landingImage"
        )

        if image:

            image_url = (
                image.get("data-old-hires")
                or image.get("src")
            )

            response = requests.get(
                image_url,
                headers=self.user_agent
            )

            with open("Product.jpg", "wb") as file:
                file.write(response.content)

            print("Image saved successfully!")

            return image_url

        return None
```

---

## 📚 What I Learned From This Project

This project provides practical experience with:

* HTTP requests
* HTML parsing
* Web scraping
* CSS/HTML selectors
* BeautifulSoup
* HTTP headers
* Regular expressions
* String manipulation
* File handling
* Binary image data
* Object-oriented programming
* Price comparison
* Exception handling

---

## ⚠️ Disclaimer

This project is intended for **educational purposes**.

When scraping websites, respect the website's:

* Terms of Service
* `robots.txt`
* Rate limits
* Copyright restrictions
* Applicable laws and regulations

Do not use the scraper to overload websites or bypass access controls.

---

## 🔮 Future Improvements

Possible improvements include:

* [ ] Automatic price monitoring
* [ ] Price history database
* [ ] Email notifications
* [ ] WhatsApp/Telegram alerts
* [ ] Multiple product tracking
* [ ] Scheduled scraping
* [ ] CSV/Excel price reports
* [ ] Graphs showing price history
* [ ] Automatic product search
* [ ] Web dashboard
* [ ] Database integration

---

## 👨‍💻 Author

**Vivek Chauhan**

A Python project focused on learning practical **web scraping, automation, and data extraction**.

---

## ⭐ Support

If you found this project useful for learning web scraping, consider giving the repository a ⭐ on GitHub.
