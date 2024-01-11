from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from foodgram_backend.constants import DOWNLOAD_FILENAME


def download_pdf(shopping_list):
    response = HttpResponse(
        content_type='application/pdf',
    )
    response['Content-Disposition'] = (
        f'attachment; filename={DOWNLOAD_FILENAME}',
    )
    pdfmetrics.registerFont(
        ttfonts.TTFont(
            'Ubuntu-Bold',
            'pdf/fonts/Ubuntu-Bold.ttf',
        )
    )
    pdfmetrics.registerFont(
        ttfonts.TTFont(
            'Ubuntu-Regular',
            'pdf/fonts/Ubuntu-Regular.ttf',
        )
    )
    page = canvas.Canvas(
        response,
        pagesize=A4,
    )
    page.drawImage(
        'pdf/images/image_for_pdf.jpg',
        x=0,
        y=550,
        width=600,
        height=297,
    )
    page.setFont(
        'Ubuntu-Bold',
        18,
    )
    page.drawString(
        x=40,
        y=510,
        text='Нужно купить:',
    )
    page.setFont(
        'Ubuntu-Regular',
        14,
    )
    x = 100
    y = 470
    for index, item in enumerate(shopping_list):
        page.drawString(
            x,
            y - (index * 20),
            item,
        )
    page.save()
    return response
