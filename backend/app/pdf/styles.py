from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4

PAGE_SIZE = A4
MARGIN = 36

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    spaceAfter=20
)

H2 = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    spaceBefore=14,
    spaceAfter=8
)

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    spaceAfter=6
)

SMALL = ParagraphStyle(
    "Small",
    parent=styles["BodyText"],
    fontSize=9,
    spaceAfter=4
)
