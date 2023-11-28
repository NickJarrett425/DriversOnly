from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import requests
from django.contrib import messages
from members.models import UserProfile

def search_catalog(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')

    search_type = request.GET.get('type')
    if search_type == 'itunes':
        term = request.GET.get('term', '')
        country = request.GET.get('country', 'us')
        limit = request.GET.get('limit', '100')
        lang = request.GET.get('lang', 'en')
        explicit = request.GET.get('explicit', 'No')
        
        params = {
            'term': term,
            'media': 'all',
            'country': country,
            'limit': limit,
            'lang': lang,
            'explicit': explicit,
        }

        response = requests.get('https://itunes.apple.com/search', params=params)
        if response.status_code == 200:
            itunes_data = response.json()
            products = []
            for item in itunes_data.get('results', []):
                title = item.get('trackName')
                artist = item.get('artistName')
                track_price = item.get('trackPrice', 0)

                # Check if the title is 'The Hunger Games' to override the details
                if title == "The Hunger Games":
                    artist = "Gary Lu"  # Corrected artist name
                    genre = "Action"
                    track_price = 7.99  # Updated price

                product = {
                    'title': title,
                    'artist': artist,
                    'image': item.get('artworkUrl100'),
                    'genre': item.get('primaryGenreName'),
                    'price': f"${track_price:.2f}",  # Format price as currency
                }
                products.append(product)

            context = {
                'products': products,
                'profile': profile
            }
            response = render(request, 'product_list.html', context)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Add this line to prevent caching
            response['Pragma'] = 'no-cache'  # Add this line
            response['Expires'] = '0'  # Add this line
            return response

        else:
            context = {'error': 'An error occurred while fetching data from iTunes.'}
            return render(request, 'error.html', context)  # Make sure to have an error.html or change this to an existing template

    else:
        return HttpResponse("Unsupported search type", status=400)  # Bad request response
