from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_invoice_pdf(data: dict):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # PDF 내용 구성 (예시: 거래처명, 품목, 합계 금액)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 800, "INVOICE / TRANSACTION RECORD")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Business Name: {data['business_name']}")
    p.drawString(100, 730, f"Partner: {data['partner_name']}")
    p.drawString(100, 710, f"Total Amount: {data['total_amount']} KRW")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer