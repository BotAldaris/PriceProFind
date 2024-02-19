import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_price_kabum(product: str):
    new_product = product.replace(" ", "-")
    url = f"https://www.kabum.com.br/busca/{new_product}"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features="html.parser")
    prices_card = soup.find_all(id="__NEXT_DATA__")
    min_produto = [0, 9999999999999999999999999999999999]
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
            price_with_super_discount = 999999999999999999999999999999
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


def get_price_pichau(product: str):
    new_product = product.replace(" ", "%20")
    url = f"https://www.pichau.com.br/search?q={new_product}"


def get_value_json(key: str, dicti: dict):
    value = dicti.get(key, 99999999998)
    if value == 0:
        value = 99999999998
    return value
