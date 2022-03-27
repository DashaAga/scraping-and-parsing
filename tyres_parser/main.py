from datetime import datetime
import datetime
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36",
    "X-Is-Ajax-Request": "X-Is-Ajax-Request",
    'X-Requested-With': "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}
def get_data():
    '''
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(r.text)
    with open("r.json", "w", encoding="utf-8") as file:
        json.dump(r.json(), file, indent=4, ensure_ascii=False)
    '''
    url = "https://roscarservis.ru/catalog/legkovye/?PAGEN_1=417"
    r = requests.get(url=url, headers=headers)
    pages = r.json()["pageCount"]
    print(pages)

    data_list = []
    for page in range(1, pages + 1):
        url = f"https://roscarservis.ru/catalog/legkovye/?PAGEN_1={page}"
        r = requests.get(url=url, headers=headers)
        data = r.json()
        items = data["items"]

        possible_stores = ["discountStores", "fortochkiStores", "commonStores"]
        for item in items:
            total_amount = 0
            item_name = f'https://roscarservis.ru{item["name"]}'
            item_price = f'https://roscarservis.ru{item["price"]}'
            item_img = f'https://roscarservis.ru{item["imgSrc"]}'
            item_url = f'https://roscarservis.ru{item["url"]}'

            stores = []
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            store_name = store["STORE_NAME"]
                            store_price = store["PRICE"]
                            store_amount = store["AMOUNT"]
                            total_amount += int(store["AMOUNT"])

                            stores.append(
                                {
                                    "store_name": store_name,
                                    "store_price": store_price,
                                    "store_amount": store_amount
                                }
                            )
            data_list.append(
                {
                    "name": item_name,
                    "price": item_price,
                    "url": item_url,
                    "img_url": item_img,
                    "stores": stores,
                    "total_amount": total_amount
                }
            )

        print(f"{page} is loaded")

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"data_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

def main():
    get_data()

if __name__=="__main__":
    main()