from django.shortcuts import render
from django.http import HttpResponse, Http404
import requests

def search_catalog(request):
    search_type = request.GET.get('type')

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
            context = {'products': products}
            return render(request, 'product_list.html', context)
        else:
            context = {'error': 'An error occurred while fetching data from iTunes.'}
    else:
        return HttpResponse("Unsupported search type", status=400)  # Bad request response
        
