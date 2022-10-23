import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def pars_to_csv(url, class_text, class_date, class_title, platform):
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_colwidth', None)

    session = requests.Session()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"}

    r = session.get(url, timeout=30, headers=headers)
    with open('yandex.html', 'r') as yandex_data:
        contents = yandex_data.read()

        soup = bs(contents, "html.parser")
        text_reviews = soup.find_all('span', class_=class_text)

    date = soup.find_all("meta", attrs={'itemprop': 'datePublished'})
    title_company = 'Приморский океанариум'
    reviews = []

    for tag in text_reviews:
        review = {
            'text': str(tag.string),
            'date': '',
            'platform_id': platform,
            'company_id': title_company
        }
        reviews.append(review)
    i = 0

    for tag in date:
        date = tag['content'][:10]
        new_date = date[8:10]+'.'+date[5:7]+'.'+date[:4]
        reviews[i]['date'] = new_date
        i += 1


    df = pd.DataFrame(reviews)
    print(df)
    df.to_csv(f'reviews_{platform}.csv', encoding='utf-8')


def pars():
    # data for irecommend
    url = "https://irecommend.ru/content/primorskii-okeanarium-ostrov-russkii-vladivostok"
    class_text = 'reviewTitle'
    class_date = 'created'
    class_title = 'product-ttl-3397656'
    platform = 'irecommend.ru'
    # pars_to_csv(url, class_text, class_date, class_title, platform)

    # data for yandex
    url_2 = 'https://yandex.ru/maps/?ll=131.925901%2C43.004755&mode=poi&poi%5Bpoint%5D=131.930112%2C43.014115&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D211680110089&tab=reviews&z=14.42'
    class_text_2 = 'business-review-view__body-text'
    class_date_2 = 'datePublished'
    class_title_2 = 'orgpage-header-view__header'
    platform_2 = 'yandex'
    # pars_to_csv(url_2, class_text_2, class_date_2, class_title_2, platform_2)

    # data for tripadvisor
    url_3 = 'https://www.tripadvisor.ru/Attraction_Review-g17182817-d10859495-Reviews-Primorsky_Aquarim-Russkiy_Primorsky_Krai_Far_Eastern_District.html'
    class_text_3 = 'yCeTE'
    class_date_3 = 'RpeCd'
    class_title_3 = 'biGQs'
    platform_3 = 'tripadvisor.ru'

    # pars_to_csv(url_3, class_text_3, class_date_3, class_title_3, platform_3)
