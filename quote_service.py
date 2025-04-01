from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from QuoteGenerate import StyledInvoice, ClientInfo, InvoiceData
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 定義接收的數據結構
class ClientInfoModel(BaseModel):
    name: str
    phone: str
    date: str
    lead_time: str
    location: str
    sales: str

class PriceModel(BaseModel):
    discount: float
    gift: int

class ItemModel(BaseModel):
    no: str
    item: str
    quantity: str
    price: str
    remark: str

class InvoiceRequest(BaseModel):
    client_info: ClientInfoModel
    price: PriceModel
    items: list[ItemModel]

# 定義 API 路徑

# 配置 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的域名，如 ["http://localhost", "http://example.com"]
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法，如 ["GET", "POST"]
    allow_headers=["*"],  # 允許的 HTTP 標頭
)


@app.post("/generate-invoice/")
async def generate_invoice(request: InvoiceRequest):
    try:
        # 創建 ClientInfo 對象
        client_info = ClientInfo(
            name=request.client_info.name,
            phone=request.client_info.phone,
            date=request.client_info.date,
            lead_time=request.client_info.lead_time,
            location=request.client_info.location,
            sales=request.client_info.sales,
        )

        # 處理商品明細
        header = ["NO", "品項", "數量", "價格/元", "備註"]
        items = [header] + [[item.no, item.item, item.quantity, item.price, item.remark] for item in request.items]
        invoice_data = InvoiceData(items)

        # 創建 PDF
        pdf_file = "styled_invoice.pdf"
        fonts = {}
        icons = {}
        invoice = StyledInvoice(pdf_file, fonts, icons, client_info, invoice_data)
        price_dict = request.price.dict()
        price_dict['discount'] = float(price_dict['discount'])
        price_dict['gift'] = int(price_dict['gift'])

        invoice.create_invoice(price_dict=price_dict)

        # 回傳生成的 PDF 文件
        return FileResponse(pdf_file, media_type="application/pdf", filename=invoice.output_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 生成失敗: {str(e)}")

