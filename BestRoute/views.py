from django.shortcuts import render

from BestRoute.models import CrimeDataPoint


# import panda or google maps api here after you pip install it
# do not forget to add it to INSTALLED_APPS in RouteHome.settings


# Renders out the inital HTML form for user input
# The form is a GET form so all params will be passed through the url
# When the form is submited the params are then passed into the next url
# '/map' which calls the crime map view
def location_form(request):
    return render(request, 'pages/location-form.html')

# This view serves to render out the google map and process all the
# queries from our DB


def crime_map(request):
    # Takes in URL params passed from locataion_form
    location_a = request.GET.get('location_a', '')
    location_b = request.GET.get('location_b', '')
    scared_level = request.GET.get('scared_level', '')

    # This is an example of a Django Query with a filter
    # .order_by(month) < You can do things like this
    crimes = CrimeDataPoint.objects.all().filter(street=location_a)
    # PUT ALL OF YOUR DATA ANALYSIS HERE
    #
    #
    #

    # When you want to pass info into the template, you define them as a context variable
    # look into the crime-map.html file to get a better understanding of what
    # I am reffering to

    context = {
        # first one is for the tempalte, second one is defined in your view...
        'location_a': location_a,
        'location_b': location_b,
        'scared_level': scared_level,
        'crimes': crimes
    }
    # This renders our the crime-map.html file with all of the defined context
    # variables
    return render(request, 'pages/crime-map.html', context)