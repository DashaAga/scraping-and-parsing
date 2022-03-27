import csv
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    headers = {
        #"Accept": "image / avif, image / webp, image / apng, image / svg + xml, image / *, * / *;q = 0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36"
    }
    '''
    req = requests.get(url="https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/", headers=headers)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/page_1.html", "w", encoding="utf-8") as file:
        file.write(req.text)
'''
    with open("data/page_1.html", "rb") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    page = int(soup.find("div", class_="bx-pagination-container").find_all("a")[-2].text)

    for i in range(1, page +1):
        url = f"https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}"
        req = requests.get(url=url, headers=headers)
        with open(f"data/page_{i}.html", "w", encoding="utf-8") as file:
            file.write(req.text)
        time.sleep(2)
    return page+1

def collect_data(page):
    cur_date = datetime.now().strftime("%d_%m_%Y")
    with open(f"data_{cur_date}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Артикул",
                "Ссылка"
            )
        )
    data = []
    for page in range(1, page):
        with open(f"data/page_{page}.html", "rb") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("a", class_="product-item__link")
        for item in items_cards:
            product_articul = item.find("p", class_="product-item__articul").text.strip()
            product_url = f"https://shop.casio.ru{item.get('href')}"#href is before product-item__link class
            data.append(
                {
                    "product_article": product_articul,
                    "product_url": product_url,
                }
            )

            with open(f"data_{cur_date}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_articul,
                        product_url
                    )
                )
        print(f"Обработана страница {page}")
    with open(f"data_{cur_date}.json", "a") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    page = get_data()
    collect_data(page)
if __name__ == "__main__":
    main()