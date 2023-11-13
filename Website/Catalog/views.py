from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import requests
from django.contrib import messages
from members.models import SponsorList, UserProfile, DriverProfile, SponsorUserProfile

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
    if profile.is_driver:
        if search_type == 'itunes':
            term = request.GET.get('term', '')  # Default to an empty string if not provided
            country = request.GET.get('country', 'us')  # Default to US if not provided
            limit = request.GET.get('limit', '100')  # Default limit
            lang = request.GET.get('lang', 'en')  # Default language
            explicit = request.GET.get('explicit', 'No')  # Default to showing explicit content
            
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
                    track_price = item.get('trackPrice', 0)
                    points = int(track_price / 0.01)

                    product = {
                        'title': item.get('trackName'),
                        'artist': item.get('artistName'),
                        'image': item.get('artworkUrl100'),
                        'genre': item.get('primaryGenreName'),
                        'price': points,
                    }
                    products.append(product)
                context = {'products': products, 'profile': profile,}
                
                return render(request, 'product_list.html', context)
            else:
                context = {'error': 'An error occurred while fetching data from iTunes.'}
        else:
            return HttpResponse("Unsupported search type", status=400)  # Bad request response
    else:
        if search_type == 'itunes':
            term = request.GET.get('term', '')  # Default to an empty string if not provided
            country = request.GET.get('country', 'us')  # Default to US if not provided
            limit = request.GET.get('limit', '100')  # Default limit
            lang = request.GET.get('lang', 'en')  # Default language
            explicit = request.GET.get('explicit', 'No')  # Default to showing explicit content
            
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
                    product = {
                        'title': item.get('trackName'),
                        'artist': item.get('artistName'),
                        'image': item.get('artworkUrl100'),
                        'genre': item.get('primaryGenreName'),
                        'price': item.get('trackPrice'),
                    }
                    products.append(product)
                context = {'products': products, 'profile': profile}
                
                return render(request, 'product_list.html', context)
            else:
                context = {'error': 'An error occurred while fetching data from iTunes.'}
        else:
            return HttpResponse("Unsupported search type", status=400)  # Bad request response
        
