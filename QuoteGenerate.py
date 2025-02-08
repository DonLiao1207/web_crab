from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from datetime import datetime

class ClientInfo:
    def __init__(self, name, phone, date, lead_time, location, sales):
        self.name = name
        self.phone = phone
        self.date = date
        self.lead_time = lead_time
        self.location = location
        self.sales = sales

class InvoiceData:
    def __init__(self, items):
        self.header = items[0]  # 保留表頭
        self.items = items[1:]  # 商品資料

    def calculate_totals(self, price_dict):
        discount_percent = price_dict["折扣"]
        special_present = price_dict["贈送"]
        total = sum(int(item[3]) for item in self.items if item[3].isdigit())
        discount = round(total * discount_percent)  # 假設10%折扣
        final_total = total - discount
        return {
            "total": total,
            "discount": discount,
            "final_total": final_total,
            "gift": special_present  # 假設固定贈送金額
        }

class StyledInvoice:
    def __init__(self, filename, fonts, icons, client_info, invoice_data):
        fonts = {
        "Iansui-Regular": "font/Iansui-Regular.ttf",
        "mi": "font/MisansTC-Normal.ttf",
        "mib": "font/MisansTC-Bold.ttf"
        }
        icons = {
        "phone": "element/tel.jpg",
        "location": "element/cord.png"
        }
        today = datetime.now().strftime("%y%m%d")
        self.output_filename = f"pdf/{today}_{client_info.name}.pdf"
        self.filename = self.output_filename
        self.fonts = fonts
        self.icons = icons
        self.client_info = client_info
        self.invoice_data = invoice_data
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        self.register_fonts()

    def register_fonts(self):
        for font_name, font_path in self.fonts.items():
            pdfmetrics.registerFont(TTFont(font_name, font_path))

    def set_background(self):
        background_color = colors.HexColor("#c8c8b4")
        self.canvas.setFillColor(background_color)
        self.canvas.rect(0, 0, self.width, self.height, fill=True, stroke=False)

        
        self.canvas.setLineWidth(10)
        self.canvas.setStrokeColor(colors.black)
        # Draw lines and black area
        self.canvas.line(0, 400, 15, 410)
        self.canvas.line(self.width, 400, self.width - 15, 410)
        self.canvas.setFillColor("#000000")
        self.canvas.rect(0, 0, self.width, 400, fill=True, stroke=False)

        # Draw white content area
        border_thickness = 10
        self.canvas.setFillColor(colors.white)
        self.canvas.rect(
            border_thickness, border_thickness,
            self.width - 2 * border_thickness,
            self.height - 2 * border_thickness,
            fill=True, stroke=False
        )

    def add_title_and_client_info(self):
        # 設置修飾線條的顏色
        self.canvas.setStrokeColor("#ffff99")
        self.canvas.setLineWidth(20)  # 設置線條寬度

        # 繪製修飾線條
        text_x = 10  # 與文字對齊的起始 X 坐標
        text_y = 750  # 線條的 Y 坐標（文字底部稍下方）
        line_length = 320  # 修飾線條的長度
        self.canvas.line(text_x, text_y, text_x + line_length, text_y)  # 繪製線條

        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Iansui-Regular", 54)
        self.canvas.drawString(50, 750, "晨 予 窗 飾")

        self.canvas.setFont("mib", 14)
        self.canvas.setFillColor(colors.lightgrey)
        self.canvas.rect(0, 640, 300, 80, fill=True, stroke=False)

        self.canvas.setFillColor(colors.black)
        self.canvas.drawString(50, 690, f"業主: {self.client_info.name}")
        self.canvas.drawString(50, 660, f"聯絡電話: {self.client_info.phone}")
        self.canvas.drawString(380, 705, f"日期: {self.client_info.date}")
        self.canvas.drawString(380, 675, f"下單訂製期：約{self.client_info.lead_time}")
        self.canvas.drawString(380, 645, f"施作地點: {self.client_info.location}")

    def add_table(self, invoice_data, column_widths):
        # 組合表頭與資料
        data = [invoice_data.header] + invoice_data.items
        table = Table(data, colWidths=column_widths, rowHeights=30)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'mi'),
            ('FONTNAME', (0, 0), (-1, 0), 'mib'),
            ('FONTSIZE', (0, 0), (-1, -1), 12)  
        ]))

        # 計算表格的總高度
        _, table_height = table.wrap(self.width, self.height)

        # 設定表格頂部的固定位置，例如 500px 高度
        fixed_top_position = 600

        # 根據表格高度計算其左下角的起始 y 座標
        start_y_position = fixed_top_position - table_height

        # 繪製表格
        table.wrapOn(self.canvas, 0, 0)  # wrapOn 不影響實際繪製位置
        table.drawOn(self.canvas, (self.width - sum(column_widths)) / 2, start_y_position)

    def add_total_block(self, totals):
        self.canvas.setFillColor(colors.lightgrey)
        self.canvas.rect(350, 85, 235, 95, fill=True, stroke=False)
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("mi", 10)
        self.canvas.drawString(405, 160, "合計")
        self.canvas.drawString(455, 160, f"${totals['total']}")
        self.canvas.drawString(405, 140, "贈送")
        self.canvas.drawString(455, 140, f"${totals['gift']}")
        self.canvas.drawString(358, 120, "特殊折扣 (10%)")
        self.canvas.drawString(455, 120, f"${totals['discount']}")
        self.canvas.setFont("mi", 12)
        self.canvas.setLineWidth(0.5)
        self.canvas.line(355, 110, 530, 110)
        self.canvas.setFont("mib", 12)
        self.canvas.drawString(397, 95, "Total")
        self.canvas.drawString(455, 95, f"${totals['final_total']}")
        self.canvas.setFont("mib", 14)
        self.canvas.drawString(455, 60, f"行銷業務")
        self.canvas.setFont("mi", 12)
        sales = self.client_info.sales
        self.canvas.drawString(455, 42, sales)

    def add_contact_info(self):
        self.canvas.setFont("mi", 10)
        self.canvas.drawString(50, 150, "匯款帳戶")
        self.canvas.drawString(50, 135, "銀行代碼：(006) 合作金庫商業銀行")
        self.canvas.drawString(50, 120, "銀行帳戶：1852765-273862")
        self.canvas.drawString(50, 100, "CONTACT INFO")

        self.canvas.drawImage(self.icons['phone'], 50, 83, width=10, height=10)
        self.canvas.drawString(63, 85, "0928-712929")
        self.canvas.drawImage(self.icons['location'], 50, 67, width=11, height=11)
        self.canvas.drawString(63, 70, "台中市太平區環中東路三段391號")

    def save_pdf(self):
        self.canvas.save()

    def create_invoice(self, price_dict=None):
        self.set_background()
        self.add_title_and_client_info()
        self.add_table(self.invoice_data, [30, 200, 50, 80, 80])
        totals = self.invoice_data.calculate_totals(price_dict)
        self.add_total_block(totals)
        self.add_contact_info()
        self.save_pdf()



if __name__ == "__main__":
    fonts = {
        "Iansui-Regular": "font/Iansui-Regular.ttf",
        "mi": "font/MisansTC-Normal.ttf",
        "mib": "font/MisansTC-Bold.ttf"
    }
    icons = {
        "phone": "element/tel.jpg",
        "location": "element/cord.png"
    }
    client_info = ClientInfo(
        name="郭小姐",
        phone="09xx-xxxxxx",
        date="11/01/2024",
        lead_time="7-10個工作天",
        location="台中市梅川東路",
        sales="維尼"
    )
    price = {
        "折扣":0.1,
        "贈送":500
    }
    items = [
        ["NO", "品項", "數量", "價格/元", "備註"],
        ["1", "1F客廳落地窗-布簾", "1", "12490", ""],
        ["2", "1F客廳落地窗-紗簾", "1", "10680", ""],
        ["10", "全戶舊軌道拆除、清運費用", "1", "500", ""]
    ]
    
    invoice_data = InvoiceData(items)
    invoice = StyledInvoice("styled_invoice.pdf", fonts, icons, client_info, invoice_data)
    invoice.create_invoice(price_dict=price)
