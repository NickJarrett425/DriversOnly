from django.shortcuts import render
from .models import login_log
from django.http import HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Image 
from reportlab.lib import colors
import os
from django.conf import settings



# Create your views here.
def build_pdf_page(canvas, doc):
    rel_path = "static/logo.png"
    file_path = os.path.join(settings.STATICFILES_DIRS, rel_path)
    logo = Image(str(file_path), width=200, height=200)
    canvas.drawImage(logo)



def all_login_attempts(request):
    login_list = login_log.objects.all()
    return render(request, 'report/all_login_attempts.html',
                  {'login_list': login_list})

def all_login_attempts_download_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=logins.txt'
    login_list = login_log.objects.all()

    lines = []
    template = "{date}, {username}, {result}\n"

    for log in login_list:
        lines.append(template.format(date=log.Datestamp,username=log.username,result=log.login_success))
    response.writelines(lines)
    return response

def all_login_attempts_download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=logins.csv'

    login_list = login_log.objects.all()
    writer = csv.writer(response)
    writer.writerow(['Date& Time', 'user', 'result'])

    for log in login_list:
        writer.writerow([log.Datestamp, log.username, log.login_success])
    
    return response

def all_login_attempts_download_pdf(request):
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=letter)
    doc.build([], onFirstPage=build_pdf_page, onLaterPages=build_pdf_page)

    # Headers
    login_list = login_log.objects.all()

    table_header = ['Date and Time', 'Username', 'Login Success']

    data = [table_header]

    for log in login_list:
        formatted_date = log.Datestamp.strftime('%m-%d-%Y %H:%M')
        login_result = bool(log.login_success)
        row = [formatted_date, log.username, login_result]
        data.append(row)

    common_row_height = 25
    page_height = letter[1]
    max_rows_per_page = int((page_height - 100) / common_row_height)

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#B3B6B7")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BACKGROUND', (1, 1), (1, -1), colors.HexColor("#E6E6E6")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements = []
    elements.append(table)

    doc.build(elements)
    buff.seek(0)

    
    doc.showPage()
    



    return HttpResponse(buff, content_type='application/pdf')