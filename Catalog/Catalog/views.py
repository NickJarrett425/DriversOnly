# Import necessary modules
import requests
from django.http import JsonResponse
from django.conf import settings
import os

# Django view function
def ebay_api_data(request):
    # eBay API endpoint and  API key
    api_url = "https://api.ebay.com/commerce/catalog/v1_beta/product/"
    
    try:
        response = requests.get(api_url, headers={"Authorization": f"Bearer {settings.EBAY_API_KEY}"})

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)

        else:
            return JsonResponse({"error": "NOPE - Opps - Failed to fetch data from eBay API"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

