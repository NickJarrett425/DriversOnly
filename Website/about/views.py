from django.shortcuts import render

def about_page(request):
    team_name = "Team-06"
    team_members = ["David Bradley", "Nick Jarrett",  "Neil Kuehn", "Dhruvisha Patel", "Ryan Ivie"]
    version = 3
    release_date_day = 3
    release_date_month = 10
    release_date_year = 2023
    product_name = "OnlyDrivers"
    description = """OnlyDrivers is a web application that rewards truck drivers for safe driving behaviors. Drivers earn points for good performance \
        and can redeem them for products from their sponsor's catalog. Sponsors manage driver applications, point distribution, and product offerings. \
        The program is designed to enhance road safety and driver engagement."""

    return render(request, 'about/about_page.html', {
        "team_name" : team_name,
        "David" : team_members[0],
        "Nick" : team_members[1],
        "Neil" : team_members[2],
        "Dhruvisha" : team_members[3],
        "Ryan" : team_members[4],
        "version" : version,
        "release_date_day" : release_date_day,
        "release_date_month" : release_date_month,
        "release_date_year" : release_date_year,
        "product_name" : product_name,
        "description" : description
    })