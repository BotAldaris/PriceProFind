import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
max_value = 9999999999999999999999999999999998

def get_price_kabum(product: str):
    new_product = product.replace(" ", "-")
    url = f"https://www.kabum.com.br/busca/{new_product}"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features="html.parser")
    prices_card = soup.find_all(id="__NEXT_DATA__")
    min_produto = [0, max_value]
    for i in prices_card:
        with open("js.txt", "w") as f:
            f.write(i.text)
        data = json.loads(i.text.strip().replace("flags", ""))
        produtos = data["props"]["pageProps"]["data"]["catalogServer"]["data"]
        for produto in produtos:
            normal_price = get_value_json("price", produto)
            price_with_discount = get_value_json(
                "priceWithDiscount", produto)
            price_with_super_discount_offer = produto.get(
                "offer", {})
            price_with_super_discount = max_value
            if price_with_super_discount_offer:
                price_with_super_discount = get_value_json(
                    "priceWithDiscount", price_with_super_discount_offer)
            min_value = min(normal_price, price_with_discount,
                            price_with_super_discount)
            if min_produto[1] > min_value:
                min_produto = [produto["code"], min_value]
    print(min_produto)


def get_price_terabyte(product: str):
    new_product = product.replace(" ", "+")
    url = f"https://www.terabyteshop.com.br/busca?str={new_product}"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    productsCard =  driver.find_elements(By.CLASS_NAME,"pbox")
    min_produto = [0, max_value,""]
    count = 0
    for product in productsCard:
        count += 1
        title = product.find_element(By.TAG_NAME, 'h2').text
        href = product.find_element(By.TAG_NAME, 'a').get_attribute("href")
        value = 0
        try:
            spanInProduct: list = product.find_elements(By.TAG_NAME, 'span')
            value_string = list(filter(lambda x :  "," in x.text or "." in x.text,spanInProduct))[1].text
            value = parse_value_string(value_string)
            if(min_produto[1] > value):
                min_produto = [title,value,href]
        except:
            break
    print(min_produto)
    print(count)

def get_price_pichau(product: str):
    new_product = product.replace(" ", "%20")
    url = f"https://www.pichau.com.br/search?q={new_product}"


def get_value_json(key: str, dicti: dict):
    value = dicti.get(key, max_value)
    if value == 0:
        value = max_value
    return value

def parse_value_string(value_string : str) -> float:
    try:
        return float(value_string.split()[1].replace(".","").replace(",","."))
    except:
        print(f"Error parsing {value_string}")
    return max_value  