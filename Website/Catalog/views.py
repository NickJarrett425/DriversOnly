from django.http import JsonResponse
import requests

def search_catalog(request):
    base_url = 'https://itunes.apple.com/search?'

    # Get the query parameters from the request (e.g., ?key1=value1&key2=value2)
    default_params = 'term=game&media=software&country=us'
    query_params = request.GET.urlencode() if request.GET else default_params

    # Construct the full URL
    full_url = base_url + query_params

    # Make the request to the iTunes API
    response = requests.get(full_url)
    if response.status_code != 200:
    # Log or print error details for diagnosis
        print(f"Error {response.status_code}: {response.text}")

    # Return the API response as JSON
    return JsonResponse(response.json(), safe=False)
