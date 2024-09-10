import time
import os

import pandas as pd

from tqdm.auto import tqdm
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Config
import Util

driver = Util.init_driver()

Util.login(driver)

file_name_list = [
    ('243_link.csv'), #
    ('25_link.csv'),
    ('314_link.csv'),
    ('202_link.csv'),
    ('36_link.csv'),
    ('37_link.csv'),
    ('277_link.csv'),
    ('312_link.csv'),
    ('275_link.csv'),
    ('308_link.csv'),
    ('280_link.csv'),
    ('318_link.csv'),
]

for file_name in file_name_list:
    menu_id = int(file_name.split('_')[0])

    content_file_name = str(menu_id) + '_content.csv'
    comment_file_name = str(menu_id) + '_comment.csv'

    df_content = pd.DataFrame([], columns=['post_id', 'title', 'date', 'nickname', 'content'])
    if os.path.isfile(content_file_name):
        df_content = pd.read_csv(content_file_name)

    df_comment = pd.DataFrame([], columns=['post_id', 'nickname', 'comment'])
    if os.path.isfile(content_file_name):
        df_comment = pd.read_csv(comment_file_name)

    df_link = pd.read_csv(file_name)
    backup_count = 0

    print()
    print('File Name: {}'.format(file_name))

    for idx in tqdm(range(len(df_link))):
        proceed = df_link['proceed'][idx]
        if proceed == 1:
            continue

        backup_count += 1

        post_id = df_link['post_id'][idx]
        
        need_re_login = False
        
        title_text = None

        try:
            driver.implicitly_wait(Config.implicitly_wait_time)
            driver.get('https://cafe.naver.com/' + Config.cafe_name + '/' + str(post_id))
            driver.switch_to.frame('cafe_main')
            driver.implicitly_wait(1)

            title_text = driver.find_element(By.CLASS_NAME, 'title_text').text
        except UnexpectedAlertPresentException as e:
            if str(e)[12:29] == '삭제되었거나 없는 게시글입니다.':
                df_link.loc[idx, 'proceed'] = 1
                continue
            else:
                need_re_login = True
        except:
            try:
                WebDriverWait(driver, Config.alert_wait_time).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
                df_link.loc[idx, 'proceed'] = 1
                continue
            except:
                need_re_login = True
            
        if need_re_login:
            time.sleep(Config.re_login_wait_time)

            Util.login(driver)

            driver.implicitly_wait(Config.implicitly_wait_time)
            driver.get('https://cafe.naver.com/' + Config.cafe_name + '/' + str(post_id))
            driver.switch_to.frame('cafe_main')
            driver.implicitly_wait(1)

            title_text = driver.find_element(By.CLASS_NAME, 'title_text').text

        date = driver.find_element(By.CLASS_NAME, 'date').text[0:-6]
        nickname = driver.find_element(By.CLASS_NAME, 'nickname').text

        content = None
        try:
            content = driver.find_element(By.CLASS_NAME, 'se-main-container').text
        except:
            content = driver.find_element(By.CLASS_NAME, 'article_viewer').text

        comment_box_list = driver.find_elements(By.CLASS_NAME, 'comment_box')
        for comment_box in comment_box_list:
            try:
                comment_nickname = comment_box.find_element(By.CLASS_NAME, 'comment_nickname').text
                comment_text = comment_box.find_element(By.CLASS_NAME, 'text_comment').text.strip()
                df_comment_row = pd.DataFrame([[post_id, comment_nickname, comment_text]], columns=['post_id', 'nickname', 'comment'])
                df_comment = pd.concat([df_comment, df_comment_row])
            except:
                continue

        df_content.loc[idx] = [post_id, title_text, date, nickname, content]
        df_link.loc[idx, 'proceed'] = 1

        if backup_count >= Config.backup_preq:
            df_content.to_csv(content_file_name, encoding='utf-8-sig', index=False)
            df_comment.to_csv(comment_file_name, encoding='utf-8-sig', index=False)
            df_link.to_csv(file_name, encoding='utf-8-sig', index=False)
            backup_count = 0

    df_content.to_csv(content_file_name, encoding='utf-8-sig', index=False)
    df_comment.to_csv(comment_file_name, encoding='utf-8-sig', index=False)
    df_link.to_csv(file_name, encoding='utf-8-sig', index=False)

print()
