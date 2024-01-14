from django.shortcuts import render
from .models import about

def about_page(request):
    newestAbout = about.objects.latest('release_date')
    return render(request, 'about/about_page.html', 
                  {'newestAbout' : newestAbout})