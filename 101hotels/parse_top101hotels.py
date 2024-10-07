import requests
from bs4 import BeautifulSoup

def get_hotels_data(city, adults, checkinDate, checkoutDate, max_pages):
    data_list = []
    
    for i in range(1, max_pages):
        url = f"https://101hotels.com/main/cities/{city}?in={checkinDate}&out={checkoutDate}&adults={adults}&page={i}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            hotels = soup.find_all('article', class_='item-inner clearfix')

            for hotel in hotels:
                hotel_name = hotel.find('span', itemprop='name').get_text(strip=True)

                hotel_url = hotel.find('a', class_='has_query_params')['href']

                price_tag = hotel.find('span', class_='price-value')
                if price_tag:
                    price = price_tag.get_text(strip=True).replace(' ', '')  
                    price = int(price)
                else:
                    price = None

                data = {
                    "checkin": checkinDate,
                    "checkout": checkoutDate,
                    "guests": [
                        {
                            "adults": adults,
                            "children": []
                        }
                    ],
                    "hotels_name": hotel_name,
                    "region": city,
                    "Price": price,
                    "hotel_url": hotel_url
                }

                data_list.append(data)
        else:
            print(f"Ошибка при запросе: {response.status_code}")
    
    return data_list

# city = "moskva"
# adults = 1
# checkinDate = "03.10.2024"
# checkoutDate = "04.10.2024"
# max_pages = 2

# hotels_data = get_hotels_data(city, adults, checkinDate, checkoutDate, max_pages)
# print(hotels_data)