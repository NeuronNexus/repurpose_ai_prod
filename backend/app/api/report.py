from fastapi import APIRouter, Response
from io import BytesIO
from app.pdf.builder import build_pdf

router = APIRouter(prefix="/api/report", tags=["Report"])


@router.post("/pdf")
async def generate_pdf_report(payload: dict):
    buffer = BytesIO()
    build_pdf(buffer, payload["analysis"])

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=repurpose_report.pdf"
        },
    )
