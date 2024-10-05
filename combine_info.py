import os, sys, time
import pandas as pd
from datetime import datetime
import traceback

def get_newest_pd_content(csv_path):
    df_new = pd.read_excel(csv_path, sheet_name=2)
    pd_content = df_new.iloc[:,0]
    content = ""
    for c in pd_content:
        content += c
    return content

def get_newest_pic_url(content, csv_path):
    # 9/11 content wait handle
    df_new = pd.read_excel(csv_path, sheet_name=0)
    pic_name = df_new[df_new["類型"] == "variable"]
    url_parent = f"https://cherrytwins.com.tw/wp-content/uploads/{datetime.now().year}/{datetime.now().month:02d}/"
    pd_desc = [[], []]
    for pic_path in (pic_name["名稱"]):
        # 假設我們要查找包含 'BOSTON' 的名稱
        if pd.isna(pic_path):
            continue
        condition = pic_name["名稱"].str.contains(pic_path).dropna()
        
        # 使用布林索引來查找符合條件的行
        matching_rows = pic_name["名稱"].dropna()[condition]

        try:
            pic_path_new = str(pic_path).replace(" ", "").strip()
            pic_floder_path = os.path.join("upload_pic", pic_path_new)
            if not os.path.exists(pic_floder_path):
                continue

            pd_desc[0].append(matching_rows.index)
            pic_list = []
            pic_alt = get_pic_alt(pic_floder_path)

            for i, p in enumerate(os.listdir(pic_floder_path)):
                pic_url = f"{url_parent}{pic_path_new}_{i+1}.jpg"
                pic_list.append(pic_url)

            # print(pic_alt)           
            pd_pic = generate_img_html(pic_alt, pic_list)
            pd_desc[1].append(pd_pic)
        except FileNotFoundError:
            print(traceback.format_exc())
            continue

    return pd_desc

def generate_img_html(alt_text, pic_list):
    # 生成 HTML 圖片語法
    pd_pic = ""
    for i, img_url in enumerate(pic_list):
        pd_pic += f'<img src="{img_url}" alt="{alt_text[i]}" width="100%">'

    return pd_pic

def get_pic_alt(pic_floder_path):
    df_alt = pd.read_excel("data/short_descriptions.xlsx")
    alt_list = df_alt[df_alt["main_name"] == pic_floder_path[11:]].iloc[0].to_list()[1:]
    return alt_list

def get_tb_content(pd_desc):
    tb_content = []
    df_type = pd.read_excel("data/0911.xlsx", sheet_name=1)
    for index in pd_desc[0]:
        catego = (df_output["分類"].iloc[index].to_list())
        for c in catego:
            pd_type = c.split(",")[0]
            type_content = df_type[df_type["品牌"] == pd_type]["尺寸語法"]
            # print(type_content)
            tb_content.append(type_content)
    return tb_content

def fill_in_desc(new_content):
    content, pd_desc, tb_content = new_content
    
    for i, desc in enumerate(pd_desc[1]):
        tb = tb_content[i].to_list()[0]
        df_output.loc[pd_desc[0][i], "商品說明"] = tb + desc
        df_output.loc[pd_desc[0][i], "商品簡短描述"] = content

    df_output.to_excel("0918_output.xlsx", index=False)

if __name__ == '__main__':
    csv_path = "data/0911.xlsx"
    df_output = pd.read_excel(csv_path)

    content = get_newest_pd_content(csv_path)
    desc = get_newest_pic_url(content, csv_path)
    tb_content = get_tb_content(desc)
    df_output = fill_in_desc([content, desc, tb_content])
    
    