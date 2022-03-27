import img2pdf
import requests

def convert_to_pdf(list):
    with open("result.pdf", "wb") as f:
        f.write(img2pdf.convert(list))
    print("PDF file is created")

def get_data():
    headers = {
        "Accept": "image / avif, image / webp, image / apng, image / svg + xml, image / *, * / *;q = 0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36"
    }
    img_list = []
    for i in range(1, 49):
        url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
        req = requests.get(url=url, headers=headers)
        response = req.content #возвращает контент в байтах

        with open(f"media/{i}.jpg", "wb") as file: #флаг wb для записи в двоичном формате
            file.write(response)
            img_list.append(f"media/{i}.jpg")
        print(f"{i} is downlpaded")
    convert_to_pdf(img_list)

def main():
    get_data()

if __name__ == '__main__':
    main()