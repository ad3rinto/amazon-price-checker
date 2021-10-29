import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
YOUR_EMAIL = ""
YOUR_PASSWORD = ""

url = "https://www.amazon.co.uk/Xiaomi-Redmi-Note-Pro-Smartphone/dp/B08XM1ZJQ8/ref=sr_1_4"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 OPR/79.0.4143.61",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("£")[1]
price_as_float = float(price_without_currency)
print(price_as_float)


title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )
