from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

# 設定字體路徑
lr_font = "font/Iansui-Regular.ttf"
font_mi_path = "font/MisansTC-Normal.ttf"
font_mib_path = "font/MisansTC-Bold.ttf"
# 註冊支援 Unicode 的字型（例如 Segoe UI Emoji）
pdfmetrics.registerFont(TTFont("Iansui-Regular", lr_font))
pdfmetrics.registerFont(TTFont("mi", font_mi_path))
pdfmetrics.registerFont(TTFont("mib", font_mib_path))

# 建立 PDF 檔案
c = canvas.Canvas("styled_invoice.pdf", pagesize=A4)
def background_setting():
    # 定義米色背景顏色
    background_color = colors.HexColor("#c8c8b4")  # 米色 (Pale goldenrod)

    width, height = A4
    print(width, height)
    # 繪製整個頁面米色背景
    c.setFillColor(background_color)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    c.setLineWidth(10)               # 邊框線寬
    # Line1 slope side
    x1, y1 = 0, 400  # 頂點1
    x2, y2 = 15, 410  # 頂點2
    c.line(x1, y1, x2, y2) 
    # 設定顏色和線寬
    c.setStrokeColor(colors.black)  # 邊框顏色

    # Line2 slope side
    x1, y1 = width, 400  # 頂點1
    x2, y2 = width - 15, 410  # 頂點2
    c.line(x1, y1, x2, y2) 
    # 設定顏色和線寬
    c.setStrokeColor(colors.black)  # 邊框顏色

    # Fill Black area
    c.setFillColor("#000000")
    c.rect(0, 0, width, 400, fill=True, stroke=False)

    # 繪製白色內容區域
    border_thickness = 10  # 邊框厚度
    content_x = border_thickness
    content_y = border_thickness
    content_width = width - 2 * border_thickness
    content_height = height - 2 * border_thickness

    c.setFillColor(colors.white)
    c.rect(content_x, content_y, content_width, content_height, fill=True, stroke=False)

background_setting()

# 標題與公司資訊區塊
c.setFillColor(colors.black)
c.setFont("Iansui-Regular", 54)
c.drawString(50, 750, "晨 予 窗 飾")

c.setFont("mib", 12)

# 繪製背景色塊

c.setFillColor(colors.lightgrey)
c.rect(0, 640, 300, 80, fill=True, stroke=False)

c.setFillColor(colors.black)
c.setFont("mib", 14)
c.drawString(50, 690, "業主: 郭小姐")
c.drawString(50, 660, "聯絡電話:09xx-xxxxxx")

c.drawString(380, 705, "日期: 11/01/2024")
c.drawString(380, 675, "下單訂製期：約7-10個工作天")
c.drawString(380, 645, "施作地點: 台中市梅川東路")
c.setFont("mi", 14)
# 商品明細表格
data = [
    ["NO", "品項", "數量", "價格/元", "備註"],
    ["1", "1F客廳落地窗-布簾", "1", "12490", ""],
    ["2", "1F客廳落地窗-紗簾", "1", "10680", ""],
    # ... (添加其他商品資料)
    ["10", "全戶舊軌道拆除、清運費用", "1", "500", ""]
]
table_column = [30, 200, 50, 80, 80]
table = Table(data, colWidths=[30, 200, 50, 80, 80], rowHeights=30)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),     # 垂直置中
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'mi')
]))
table_margin = (595.2756 - sum(table_column))/2
table.wrapOn(c, table_margin, 500)
table.drawOn(c, table_margin, 500)

# 金額總計區塊
c.setFillColor(colors.lightgrey)
c.rect(350, 85, 235, 95, fill=True, stroke=False)
c.setFillColor(colors.black)
c.setFont("mi", 10)
c.drawString(405, 160, "合計")
c.drawString(455, 160, "$103240")
c.drawString(405, 140, "贈送")
c.drawString(455, 140, "$550")
c.drawString(358, 120, "特殊折扣(10%)")
c.drawString(455, 120, "$10269")
c.setFont("mi", 12)
c.setLineWidth(0.5)
c.line(355, 110, 530, 110)
c.setFont("mib", 12)
c.drawString(397, 95, "Total")
c.drawString(455, 95, "$92421")

c.setFont("mib", 14)

c.drawString(455, 60, f"行銷業務")
c.setFont("mi", 12)
sales = "維尼"
c.drawString(455, 42, sales)

# 聯絡資訊與匯款帳戶
c.setFont("mi", 10)
c.drawString(50, 150, "匯款帳戶")
c.drawString(50, 135, "銀行代碼：(006) 合作金庫商業銀行")
c.drawString(50, 120, "銀行帳戶：1852765-273862")
c.drawString(50, 100, "CONTACT  INFO")
# 加入電話和定位圖示
location_icon = ImageReader('element/cord.png')  # 替換為定位圖示的檔案路徑
phone_icon = ImageReader('element/tel.jpg')  # 替換為電話圖示的檔案路徑
# 放置圖示
c.drawImage(phone_icon, 50, 83, width=10, height=10)  # 調整位置與大小
c.drawString(63, 85, "0928-712929")

c.drawImage(location_icon, 50, 67, width=11, height=11)  # 調整位置與大小
c.drawString(63, 70, "台中市太平區環中東路三段391號")

# 保存 PDF
c.save()
