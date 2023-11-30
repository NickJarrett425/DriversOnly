from django.shortcuts import render, redirect
from django.contrib import messages
from .models import login_log
from members.models import UserProfile
from django.http import HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Image,PageTemplate,Frame,Paragraph,PageBreak,Spacer 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.conf import settings
import datetime
from .forms import report_filtering



def report_home(request):
    if request.method == "POST":
        report_form = report_filtering(request.POST)                
        if report_form.is_valid():
            report_type = report_form.cleaned_data['report_type']
            user = report_form.cleaned_data['user']
            start_date_range = report_form.cleaned_data['start_date_range']
            end_date_range = report_form.cleaned_data['end_date_range']
            if(report_type == 1):
                response = all_login_attempts_download_pdf(request)
                return(response)
    elif request.method == "GET":
        context = {}
        context['form'] = report_filtering
        return render( request, "report/home.html", context)


# Create your views here.
def build_pdf_page(canvas, doc):

    width, height = letter
    
    styles = getSampleStyleSheet()  
    title_style = styles['Title']
    title_style.alighnment = 1

    title = Paragraph(doc.title, title_style)    

    text_width = title.wrap(width, height)[0]
    x = (width - text_width) / 2
    y = height - inch 

    title.drawOn(canvas, x, y)

    img_dem = 80
    rel_path = "logo_white_background.png"
    file_path = os.path.join(settings.STATICFILES_DIRS[0], rel_path)
    canvas.drawImage(file_path,x=0,y=(800-img_dem),width=img_dem,height=img_dem,preserveAspectRatio=True,anchor='ne')

    footer_string = "Page Number:" + str(canvas.getPageNumber()) 
    footer_style = styles["Normal"]
    footer_style.alignment = 2
    footer = Paragraph(footer_string)
    footer_w,footer_h = footer.wrap(width,height)
    y = footer_h
    footer.drawOn(canvas,500,y)




def all_login_attempts(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view reports.")
        return redirect('/')
    user = request.user

    if user.is_superuser:
        login_list = login_log.objects.all()
        return render(request, 'report/all_login_attempts.html',
                    {'login_list': login_list})
    else:
        return redirect('/about')

def all_login_attempts_download_txt(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view reports.")
        return redirect('/')
    user = request.user

    if user.is_superuser:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=logins.txt'
        login_list = login_log.objects.all()

        lines = []
        template = "{date}, {username}, {result}\n"

        for log in login_list:
            lines.append(template.format(date=log.Datestamp,username=log.username,result=log.login_success))
        response.writelines(lines)
        return response
    else:
        return redirect('/about')


def all_login_attempts_download_csv(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view reports.")
        return redirect('/')
    user = request.user

    if user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=logins.csv'

        login_list = login_log.objects.all()
        writer = csv.writer(response)
        writer.writerow(['Date& Time', 'user', 'result'])

        for log in login_list:
            writer.writerow([log.Datestamp, log.username, log.login_success])
        
        return response
    else:
        return redirect('/about')


def generate_pdf(title,data):
    buff = io.BytesIO()
    current_date = datetime.datetime.today()
    formatted_date = current_date.strftime("%m-%d-%Y")
    report_title = title + " " + formatted_date
    doc = SimpleDocTemplate(buff, pagesize=letter, title=report_title)

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


    doc.build(
        elements,
        onFirstPage=build_pdf_page,
        onLaterPages=build_pdf_page
    ) 

    buff.seek(0)  

    return HttpResponse(buff, content_type='application/pdf')

def all_login_attempts_download_pdf(request):    
    login_list = login_log.objects.all()

    table_header = ['Date and Time', 'Username', 'Login Success'] # Headers

    data = [table_header]

    for log in login_list:
        formatted_date = log.Datestamp.strftime('%m-%d-%Y %H:%M')
        login_result = bool(log.login_success)
        row = [formatted_date, log.username, login_result]
        data.append(row)

    response = generate_pdf("Login Attempts Report",data)
    return (response)

def all_user_login_attempts(request,user):
    #user is expected to be a string not an object

    login_list = login_log(user=user)
    table_header = ['Date and Time', 'Login Success'] # Headers
    data = [table_header]

    for log in login_list:
        formatted_date = log.Datestamp.strftime('%m-%d-%Y %H:%M')
        login_result = bool(log.login_success)
        row = [formatted_date, login_result]
        data.append(row)
    
    title = user + "Login Attempts Report"
    response = generate_pdf(title,data)
    return(response)

def all_date_range_login_attempts(request,start_range,end_range):
    #ranges are expected to be strings

    login_list = login_log(date__range=[start_range,end_range])
    table_header = ['Date and Time', 'Username', 'Login Success'] # Headers
    data = [table_header]

    for log in login_list:
        formatted_date = log.Datestamp.strftime('%m-%d-%Y %H:%M')
        login_result = bool(log.login_success)
        row = [formatted_date, log.username, login_result]
        data.append(row)
    
    title = "Login Attempts Report in a date range - Generated:"
    response = generate_pdf(title,data)
    return(response)
