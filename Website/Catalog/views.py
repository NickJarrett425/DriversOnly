from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from urllib.parse import unquote
import requests
from django.contrib import messages
from members.forms import ChooseSponsorForm
from members.models import UserProfile, SponsorList, SponsorUserProfile

def choose_catalog(request):
    user_sponsors = SponsorList.objects.filter(sponsored_users__user=request.user)

    if request.method == "POST":
        form = ChooseSponsorForm(request.POST, sponsor_queryset=user_sponsors)
        if form.is_valid():
            selected_sponsor_id = form.cleaned_data['sponsor_choices']
            selected_sponsor = SponsorList.objects.get(id=selected_sponsor_id)
            
            # Perform actions with the selected sponsor, for example, store it in the session
            request.session['selected_sponsor'] = selected_sponsor.sponsor_name
            return redirect('search_catalog')
    else:
        form = ChooseSponsorForm(sponsor_queryset=user_sponsors)

    context = {
        'form': form,
    }
    return render(request, 'choose_catalog.html', context)

def search_catalog(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')

    request.session['last_search_url'] = request.get_full_path()
    search_type = 'itunes'

    if search_type == 'itunes':
        search_query = request.GET.get('search', '')
        country = request.GET.get('country', 'us')
        limit = request.GET.get('limit', '100')
        lang = request.GET.get('lang', 'en')
        explicit = request.GET.get('explicit', 'No')
        
        params = {
            'term': search_query,
            'media': 'all',
            'country': country,
            'limit': limit,
            'lang': lang,
            'explicit': explicit,
        }
        if profile.is_driver:
            sponsor_name = request.session.get('selected_sponsor')
            sponsor = SponsorList.objects.get(sponsor_name=sponsor_name)
        elif profile.is_sponsor:
            sponsor_user = SponsorUserProfile.objects.get(user=request.user)
            sponsor = SponsorList.objects.get(sponsor_name=sponsor_user.sponsor_name)
        
        response = requests.get('https://itunes.apple.com/search', params=params)
        if response.status_code == 200:
            itunes_data = response.json()
            products = []
            matched_artist_results = []
            other_results = []

            for item in itunes_data.get('results', []):
                title = item.get('trackName')
                artist = item.get('artistName')
                image_url = item.get('artworkUrl100')
                new_url = image_url.replace('100x100bb.jpg', '600x600bb.jpg')
                    
                track_price = item.get('trackPrice', 0)
                if profile.is_driver:
                    point_conversion = sponsor.point_conversion
                    track_price = int(track_price / point_conversion)

                # Check if the title is 'The Hunger Games' to override the details
                if title == "The Hunger Games":
                    artist = "Gary Lu"  # Corrected artist name
                    genre = "Action"
                    track_price = 7.99  # Updated price
                    if profile.is_driver:
                        track_price = int(track_price / point_conversion)

                product = {
                    'title': title,
                    'artist': artist,
                    'image': new_url,
                    'genre': item.get('primaryGenreName'),
                    'price': track_price
                }

                # Prioritize results where the artist's name matches the search query
                if search_query.lower() in artist.lower():
                    matched_artist_results.append(product)
                else:
                    other_results.append(product)

            # Combine the matched artist results and other results
            sorted_products = matched_artist_results + other_results

            for product in sorted_products:
                if product['price'] > 0:
                    products.append(product)

            if profile.is_driver or profile.is_sponsor:
                context = {
                    'products': products,
                    'profile': profile,
                    'term': search_query,
                    'sponsor': sponsor,
                }
            elif request.user.is_superuser:
                context = {
                    'products': products,
                    'profile': profile,
                    'term': search_query,
                }
            response = render(request, 'product_list.html', context)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        else:
            context = {'error': 'An error occurred while fetching data from iTunes.'}
            return render(request, 'error.html', context)

    else:
        return HttpResponse("Unsupported search type", status=400)
    
def view_item(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    
    title = unquote(request.GET.get('title', ''))
    artist = unquote(request.GET.get('artist', ''))
    image = unquote(request.GET.get('image', ''))
    genre = unquote(request.GET.get('genre', ''))
    price = unquote(request.GET.get('price', ''))
    last_search_url = request.session.get('last_search_url')

    resized_image = image.replace('600x600bb.jpg', '450x450bb.jpg')

    context = {
        'title': title,
        'artist': artist,
        'image': resized_image,
        'genre': genre,
        'price': price,
        'profile': profile,
        'last_search_url': last_search_url,
        # Any additional data you want to send to the template
    }
    return render(request, 'view_item.html', context)
