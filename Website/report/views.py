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


# Create your views here.

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

def all_login_attempts_download_pdf(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view reports.")
        return redirect('/')
    user = request.user

    if user.is_superuser:
        buff = io.BytesIO()
        can = canvas.Canvas(buff, pagesize=letter, bottomup=0)
        textobj = can.beginText()
        textobj.setTextOrigin(inch,inch)
        textobj.setFont("Times-Roman", 12)

        lines = []
        login_list = login_log.objects.all()

        for log in login_list:
            lines.append(str(log.Datestamp))
            lines.append(log.username)
            lines.append(str(log.login_success))
            lines.append(" ")

        for line in lines: 
            textobj.textLine(line)

        can.drawText(textobj)
        can.showPage()
        can.save()
        buff.seek(0)
        
        return FileResponse(buff, as_attachment=True, filename='logins.pdf')
    else:
        return redirect('/about')