# 安裝需求：pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from WooUploadAPI import WooCommerceUploader
import re
from datetime import datetime
import basic_html

class WababeScraper:
    def __init__(self):
        self.base_url = "https://wababewa.com/collections/-new-7"
        self.uploader = WooCommerceUploader(
            wc_url="https://cherrytwins.com.tw/wp-json/wc/v3/products",
            consumer_key="ck_d46a4130192b19023b22a28cec315f1001d5f196",
            consumer_secret="cs_61c3a3cbb6e62420a4b6628f6c1f644a080a7ccb"
        )

    def scrape_all_pages(self):
        all_products = []
        for page in range(1, 2):
            params = {"limit": 50, "page": page, "sort": "position+desc"}
            response = requests.get(self.base_url, params=params)
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".product_grid-item")

            for item in items:
                link_tag = item.select_one("a.grid-link__image-centered")
                title_tag = item.select_one(".grid-link__title")
                if not link_tag:
                    continue

                href = link_tag["href"]
                full_url = f"https://wababewa.com{href}"
                name = title_tag.get_text(strip=True) if title_tag else "無商品名稱"

                # 進入商品頁面抓圖片、description、尺寸、價格
                product_data = self.scrape_product_page(full_url)
                cover_image = product_data["images"][0] if product_data["images"] else ""
                month_tag = datetime.now().strftime("%Y-%m")
                alt_text = f"日本童裝推薦, 韓國童裝推薦--{month_tag}月韓國日本童裝預購, 2-10歲童裝"

                img_tags = "\n".join([
                    f'<img src="{url.replace("&amp;", "&")}" alt="{alt_text}" width="100%" />'
                    for url in product_data["images"]
                ])

                description_html = basic_html.BRAND_NOTICE_HTML + "<br><br>" + img_tags

                sizes, colors, prices = [], [], []
                for s in product_data["sizes"]:
                    parts = s.split(", ", 1) 
                    size = parts[0].strip()
                    sizes.append(size)

                    if len(parts) == 2:
                        color = parts[1].strip()
                        clean_color = re.sub(r"\s*-NT\$[\s]*[\d,\.]+", "", color).strip()
                        colors.append(clean_color)

                # 如果沒有顏色資料，補上一個固定值
                if not colors:
                    colors = ["單一顏色"]

                sizes = list(set(sizes))
                colors = list(set(colors))

                # 建立父商品
                pid = self.uploader.create_variable_product(
                    name=name,
                    description_html=description_html,
                    image_urls=[cover_image],
                    sizes=sizes,
                    colors=colors
                )

                # 建立變體
                if pid:
                    for i, s in enumerate(product_data["sizes"]):
                        parts = s.split(", ", 1)
                        size = parts[0].strip()
                        if len(parts) == 2:
                            color = re.sub(r"\s*-NT\$[\s]*[\d,\.]+", "", parts[1].strip())
                        else:
                            color = "單一顏色"

                        price = product_data["prices"][i] if i < len(product_data["prices"]) else "400"
                        self.uploader.create_variations(pid, [size], [color], price=price)
                if product_data:
                    product_data["name"] = name
                    product_data["url"] = full_url
                    all_products.append(product_data)
                else:
                    print("⚠️ 無法解析商品頁：", full_url)

        return all_products

    def scrape_product_page(self, url):
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            # 圖片 from gallery
            images = [
                li["data-mfp-src"]
                for li in soup.select("ul.gallery li.gallery__item")
                if li.get("data-mfp-src")
            ]

            # description html
            desc_tag = soup.select_one("div.product-description .fr-view")
            description_html = str(desc_tag) if desc_tag else ""

            # 尺寸與價格
            sizes, prices = [], []
            for option in soup.select("select#productSelect option"):
                text = option.get_text(strip=True)
                price_tag = option.select_one("span.money")
                if not price_tag:
                    continue
                price_raw = price_tag.get("data-ori-price", "0").replace(",", "")
                price = str(int(float(price_raw) / 100))  # 換算為台幣整數
                size = text.split(" - ")[0].strip()
                sizes.append(size)
                prices.append(price)

            return {
                "images": images,
                "description_html": description_html,
                "sizes": sizes,
                "prices": prices
            }

        except Exception as e:
            print("⚠️ 商品頁解析失敗：", url, e)
            return None

# === 測試 ===
if __name__ == "__main__":
    scraper = WababeScraper()
    products = scraper.scrape_all_pages()