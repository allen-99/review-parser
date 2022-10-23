import pandas as pd
import sqlite3

from datetime import datetime


def db_insert(conn, platform_name):
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_colwidth', None)

    try:
        id_platform = pd.read_sql("SELECT platform_id FROM platform where platform_name = :pn", conn,
                                  params={"pn": f'{platform_name}.ru'})

        is_here = pd.read_sql("""SELECT platform_id, company_id 
                                        FROM text 
                                        where platform_id = :pn and company_id = 1
                                        """, conn, params={"pn": int(id_platform['platform_id'])})

        reviews = pd.read_csv(f"reviews_{platform_name}.csv", sep=',',  index_col=0)
        # for yandex only platform_name, for else with '.ru'
        if platform_name == 'yandex':
            reviews = reviews.replace(f'{platform_name}', int(id_platform['platform_id']))
            reviews = reviews.replace('Приморский океанариум', 1)
        else:
            reviews = reviews.replace(f'{platform_name}.ru', int(id_platform['platform_id']))
            reviews = reviews.replace('Приморский океанариум (остров Русский), Владивосток', 1)
        new_date = []
        for indx, x in enumerate(reviews.values):
            value = reviews.values[indx][0][6:]\
                                      +'-'+reviews.values[indx][0][3:5]+'-'+reviews.values[indx][0][:2]
            value = datetime.strptime(value, "%Y-%m-%d")
            new_date.append(value)

        reviews['date'] = new_date

        if is_here.empty:
            reviews.to_sql('text', conn, if_exists='append')

    except Exception as e:
        print(e)


#  метод, в котором запросы: необходимые для заданния
#  вывожу без текста, потому что его много и занимает много места (вместо него id)
def db_requests(conn):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # 1 запрос. Вывести все отзывы с площадки Яндекс отсортированные по возрастанию
    result_1 = pd.read_sql("""select id,  date, platform_name, company_name from text
                            inner join company on text.company_id = company.company_id
                            inner join platform on text.platform_id = platform.platform_id
                            where platform_name = 'yandex.ru'
                            order by date
                            """, conn)
    # print(result_1)

# 2 запрос. Вывести все отзывы и сколько дней прошло с моменты их написания на площадке irecommend.ru
# отсортированные по возрастанию этих дней
    result_2 = pd.read_sql("""select id,
                                    date, 
                                    platform_name, 
                                    company_name,
                                    CAST(julianday('now') - julianday(date) as integer) as 'day_count'
                            from text
                            inner join company on text.company_id = company.company_id
                            inner join platform on text.platform_id = platform.platform_id
                            where platform_name = 'irecommend.ru'
                            order by day_count
                            """, conn)
    # print(result_2)

# 3 запрос. Вывести название площадки и сумму отзывов по каждой из них, длина текста которых не превышает 500 символов
    result_3 = pd.read_sql("""select 
                                platform_name, count(*) as 'count_reviews'
                                from text
                                inner join platform on text.platform_id = platform.platform_id
                                where length(text) <= 500
                                group by platform_name
                                """, conn)
    print(result_3)


def db():
    conn = sqlite3.connect('identifier.sqlite')

    # db_insert(conn, 'irecommend')
    # db_insert(conn, 'tripadvisor')
    # db_insert(conn, 'yandex')

    db_requests(conn)

    conn.close()


if __name__ == '__main__':
    db()
