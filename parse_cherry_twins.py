import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
df_pd = pd.read_excel(r'/home/sram-admin/workspace/web_crab/0902.xlsx')
df_tb = pd.read_excel(r'/home/sram-admin/workspace/web_crab/0902.xlsx', sheet_name=1)
df_alt = pd.read_excel(r'/home/sram-admin/workspace/web_crab/0902.xlsx', sheet_name=2)

df_dict = {"名稱":[], "圖片":[]}

df_pd_main = df_pd[df_pd['類型'] == "variable"]

def crab_pic(df_pd_main):
    for i in range(len(df_pd_main)):
        url = df_pd_main.iloc[i]['圖片']
        if 'wababewa' in url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_='slide-img product-zoomable mfp-Images')
            img_srcs = [div.find('img')['src'] for div in divs if div.find('img')]
            print(img_srcs)
            os.makedirs(df_pd_main.iloc[i]['名稱'].strip(), exist_ok=True)
            for img_i, img_src in enumerate(img_srcs):
                img_data = requests.get(img_src).content
                img_file = os.path.join(df_pd_main.iloc[i]['名稱'], f"image_{img_i+1}.jpeg")
                with open(img_file, 'wb') as handler:
                    handler.write(img_data)
                print(f"下載完成: {img_file}")

crab_pic(df_pd_main)