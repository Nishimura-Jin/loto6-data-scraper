import time #DOS攻撃防止用
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

loto_url1 = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/backnumber/loto6' # 1～460回目
loto_url2 = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/backnumber/detail.html?fromto=' # 461回目以降
num = 1

main_num_list = [] # 本数字6桁を格納するリスト
bonus_num_list = [] # ボーナス数字を格納するリスト

op = Options()
op.add_argument("--headless")
op.add_argument('--disable-gpu')
op.add_argument('--no-sandbox')
op.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')

op.add_argument("-window-size=1280,1024")
op.add_argument('--blink-settings=imagesEnabled=false')
op.add_argument('--ignore-certificate-errors')
op.add_argument('--allow-running-insecure-content')
op.add_argument('--disable-web-security')
# headlessでは不要そうな機能
op.add_argument('--disable-desktop-notifications')
op.add_argument("--disable-extensions")
# 言語
op.add_argument('--lang=ja')
# 画像を読み込まないで軽くする
op.add_argument('--blink-settings=imagesEnabled=false')

# ロト6の当選番号が掲載されているみずほ銀行ページのURL


driver = webdriver.Chrome('./chromedriver', options=op)


while num <= 2060: #取得したい回数を入れる

  # 第1～460回目までの当選ページのURL
    if num < 461:
        url = loto_url1 + str(num).zfill(4) + '.html'
  # 461回目以降当選ページのURL
    else:
        url = loto_url2 + str(num) + '_' + str(num+19) + '&type=loto6'

    driver.get(url)

    time.sleep(5)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    # ロト6の当選番号がのっているテーブルの取得
    table = soup.find_all("table")
    del table[0]

    for i in table:
    # 本数字の取得
        main_num = i.find_all("tr")[2].find("td")
        main_num_list.append(main_num.string.split(" "))

        # ボーナス数字の取得
        bonus_num = i.find_all("tr")[3].find("td")
        bonus_num_list.append(bonus_num.string)

    num += 20 # 次のページに移動するためにnumに20を追加
    time.sleep(random.uniform(1, 3)) # 1～3秒Dos攻撃にならないようにするためにコードを止める

# csvで出力
df = pd.DataFrame(main_num_list, columns = ['main1', 'main2', 'main3', 'main4', 'main5', 'main6'])
df['bonus'] = bonus_num_list
df.index = df.index + 1
df.to_csv('loto6.csv')
