import pandas as pd

from tqdm.auto import tqdm
from bs4 import BeautifulSoup as bs

import Config
import Util

driver = Util.init_driver()

Util.login(driver)

menu_id_page = [
    (243, 382), #
    (25, 623),
    (314, 6),
    (202, 5),
    (36, 27),
    (37, 17),
    (277, 8),
    (312, 71),
    (275, 90),
    (308, 50),
    (280, 84),
    (318, 25),
]

for menu_id, num_page in menu_id_page:
    df_link = pd.DataFrame([], columns=['post_id', 'proceed'])

    print()
    print('Menu ID: {}'.format(menu_id))

    for page in tqdm(range(num_page)):
        driver.implicitly_wait(Config.implicitly_wait_time)
        driver.get('https://cafe.naver.com/ArticleList.nhn?search.clubid=' + str(Config.cafe_id)
                    + '&search.menuid=' + str(menu_id)
                    + '&userDisplay=50&search.boardtype=L&search.totalCount=151&search.cafeId=' + str(Config.cafe_id)
                    + '&search.page=' + str(page + 1))
        driver.switch_to.frame('cafe_main')
        driver.implicitly_wait(1)

        soup = bs(driver.page_source, 'html.parser')

        article = soup.find('div', attrs={'class':'article-board m-tcol-c', 'id':''}).find_all(class_='inner_list')

        for idx in range(len(article)):
            post_id = article[idx].find(class_='article')['href'].split('articleid=')[-1].split('&')[0]
            df_link_row = pd.DataFrame([[int(post_id), 0]], columns=['post_id', 'proceed'])
            df_link = pd.concat([df_link, df_link_row])

    df_link.to_csv(str(menu_id) + '_link.csv', encoding='utf-8-sig', index=False)

print()
