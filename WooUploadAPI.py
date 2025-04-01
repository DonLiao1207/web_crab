import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import basic_html

class WooCommerceUploader:
    def __init__(self, wc_url, consumer_key, consumer_secret):
        self.wc_url = wc_url
        self.auth = HTTPBasicAuth(consumer_key, consumer_secret)

    def create_variable_product(self, name, description_html, image_urls, sizes, colors):
        attributes = [
            {
                "name": "尺寸",
                "visible": True,
                "variation": True,
                "options": sizes
            },
            {
                "name": "顏色",
                "visible": True,
                "variation": True,
                "options": colors
            }
        ]

        product_data = {
            "name": name,
            "type": "variable",
            "description": description_html,
            "images": [{"src": url} for url in image_urls],
            "attributes": attributes,
            "stock_status": "instock",
            "status": "pending",  # ✅ 設定為「待審閱」
            "short_description": basic_html.SHORT_DESCRIPTION_HTML
        }

        create_response = requests.post(self.wc_url, auth=self.auth, json=product_data)
        product = create_response.json()
        product_id = product.get("id")

        if not product_id:
            print("父商品建立失敗：", product)
            return None

        print(f"✅ 父商品建立成功，ID: {product_id}")
        return product_id

    def create_variations(self, product_id, sizes, colors, price="380", stock=10):
        variation_url = f"{self.wc_url}/{product_id}/variations"
        for size in sizes:
            for color in colors:
                variation_data = {
                    "regular_price": price,
                    "manage_stock": False,
                    "stock_quantity": stock,
                    "in_stock": True,           # 明確標示這個變體是有貨的
                    "attributes": [
                        {"name": "尺寸", "option": size},
                        {"name": "顏色", "option": color}
                    ]
                }
                v_response = requests.post(variation_url, auth=self.auth, json=variation_data)
                if v_response.status_code == 201:
                    print(f"✅ variation {size} / {color} 建立成功")
                else:
                    print(f"❌ variation {size} / {color} 建立失敗：", v_response.text)

# === 使用範例 ===
if __name__ == "__main__":
    uploader = WooCommerceUploader(
        wc_url="https://cherrytwins.com.tw/wp-json/wc/v3/products",
        consumer_key="ck_d46a4130192b19023b22a28cec315f1001d5f196",
        consumer_secret="cs_61c3a3cbb6e62420a4b6628f6c1f644a080a7ccb"
    )

    # 測試商品資料
    name = "測試商品"
    images = [
        "https://cdn.store-assets.com/s/400709/i/85013901.jpeg",
        "https://cdn.store-assets.com/s/400709/i/85013902.jpeg"
    ]
    sizes = ["5", "7", "9"]
    colors = ["米白"]
    description_html = """
    <p>這是一個測試商品，含有尺寸與顏色選項。</p>
    <img src='https://cdn.store-assets.com/s/400709/i/85013901.jpeg' width='100%'>
    <img src='https://cdn.store-assets.com/s/400709/i/85013902.jpeg' width='100%'>
    """

    pid = uploader.create_variable_product(name, description_html, images, sizes, colors)
    if pid:
        uploader.create_variations(pid, sizes, colors)
