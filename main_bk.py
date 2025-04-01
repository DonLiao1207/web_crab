import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import A4
from QuoteGenerate import StyledInvoice, ClientInfo, InvoiceData

class InvoiceGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 發票生成器")
        self.setGeometry(500, 100, 800, 800)
        main_layout = QVBoxLayout()
        
        # 客戶資訊表單
        form_layout = QGridLayout()
        
        # 客戶資訊 - 兩列顯示
        self.name_input = self.create_input_field(form_layout, "業主名稱:", "郭小姐", 0, 0)
        self.phone_input = self.create_input_field(form_layout, "聯絡電話:", "09xx-xxxxxx", 0, 1)
        self.date_input = self.create_input_field(form_layout, "日期:", "11/01/2024", 1, 0)
        self.lead_time_input = self.create_input_field(form_layout, "訂製期:", "7-10個工作天", 1, 1)
        self.location_input = self.create_input_field(form_layout, "施作地點:", "台中市梅川東路", 2, 0)
        self.sales_input = self.create_input_field(form_layout, "行銷業務:", "維尼", 2, 1)

        # 折扣與贈送
        self.discount_input = QLineEdit("0.1")
        self.gift_input = QLineEdit("500")
        form_layout.addWidget(QLabel("折扣 (%):"), 3, 0)
        form_layout.addWidget(self.discount_input, 3, 1)
        form_layout.addWidget(QLabel("贈送金額:"), 4, 0)
        form_layout.addWidget(self.gift_input, 4, 1)

        main_layout.addLayout(form_layout)

        # 商品明細表格
        main_layout.addWidget(QLabel("商品明細:"))
        self.items_table = QTableWidget(3, 5)
        self.items_table.setHorizontalHeaderLabels(["NO", "品項", "數量", "價格/元", "備註"])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 預設商品資料
        default_items = [
            ["1", "1F客廳落地窗-布簾", "1", "12490", ""],
            ["2", "1F客廳落地窗-紗簾", "1", "10680", ""],
            ["10", "全戶舊軌道拆除、清運費用", "1", "500", ""]
        ]
        for row, item in enumerate(default_items):
            for col, value in enumerate(item):
                self.items_table.setItem(row, col, QTableWidgetItem(value))
        
        main_layout.addWidget(self.items_table)

        # 新增商品行按鈕
        add_item_button = QPushButton("新增商品")
        add_item_button.clicked.connect(self.add_item_row)
        main_layout.addWidget(add_item_button)

        # 生成 PDF 按鈕
        generate_button = QPushButton("生成 PDF")
        generate_button.clicked.connect(self.generate_pdf)
        main_layout.addWidget(generate_button)

        self.setLayout(main_layout)

    def create_input_field(self, layout, label, default_value, row, col):
        layout.addWidget(QLabel(label), row, col * 2)
        line_edit = QLineEdit(default_value)
        layout.addWidget(line_edit, row, col * 2 + 1)
        return line_edit

    def add_item_row(self):
        # 新增一行空白商品資料
        row_count = self.items_table.rowCount()
        self.items_table.insertRow(row_count)
        for col in range(self.items_table.columnCount()):
            self.items_table.setItem(row_count, col, QTableWidgetItem(""))

    def get_items_data(self):
        items = [["NO", "品項", "數量", "價格/元", "備註"]]
        for row in range(self.items_table.rowCount()):
            item_row = []
            for col in range(self.items_table.columnCount()):
                item = self.items_table.item(row, col)
                item_row.append(item.text() if item else "")
            items.append(item_row)
        return items

    def generate_pdf(self):
        # 收集客戶資訊
        client_info = ClientInfo(
            name=self.name_input.text(),
            phone=self.phone_input.text(),
            date=self.date_input.text(),
            lead_time=self.lead_time_input.text(),
            location=self.location_input.text(),
            sales=self.sales_input.text()
        )
        
        # 收集折扣和贈送
        price = {
            "折扣": float(self.discount_input.text()),
            "贈送": int(self.gift_input.text())
        }

        # 收集商品明細
        items = self.get_items_data()

        # 生成 PDF
        invoice_data = InvoiceData(items)
        invoice = StyledInvoice("styled_invoice.pdf", fonts, icons, client_info, invoice_data)
        invoice.create_invoice(price_dict=price)

        # 顯示生成成功訊息
        QMessageBox.information(self, "生成成功", "PDF 已成功生成！")

if __name__ == "__main__":
    # 模擬 StyledInvoice, ClientInfo, InvoiceData 的用例
    fonts = {
        "Iansui-Regular": "font/Iansui-Regular.ttf",
        "mi": "font/MisansTC-Normal.ttf",
        "mib": "font/MisansTC-Bold.ttf"
    }
    icons = {
        "phone": "element/tel.jpg",
        "location": "element/cord.png"
    }
    
    app = QApplication(sys.argv)
    window = InvoiceGenerator()
    window.show()
    sys.exit(app.exec_())
