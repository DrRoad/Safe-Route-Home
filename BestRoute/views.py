import json
import sys
import geocoder
from pickle import dump, load
import Ellipse
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from BestRoute.models import CrimeDataPoint
from Map_Quest_Get import Send_Data
from django.core.management import execute_from_command_line
from routehome.settings import GoogleMaps_API, MapQuest_API, Google_JS_API

# import panda or google maps api here after you pip install it
# do not forget to add it to INSTALLED_APPS in RouteHome.settings


# Renders out the inital HTML form for user input
# The form is a GET form so all params will be passed through the url
# When the form is submited the params are then passed into the next url
# '/map' which calls the crime map view
def location_form(request):
    """
    Function renders the landing page for the website
    """
    return render(request, 'pages/location-form.html')

# This view serves to render out the google map and process all the
# queries from our DB


def crime_map(request):
    """
    Takes in URL params passed from location_form.
    Communicates with MapQuest and Google APIs.
    Displays information on crime-map page
    """
    # Takes in URL params passed from locataion_form
    location_a = request.GET.get('location_a', '')
    location_b = request.GET.get('location_b', '')
    filters = {
        'homicide': 'Homicide',
        'caraccident': 'Vehicle Accident',
        'oui': 'Operating Under the Influence',
        'indecentAssault': 'Indecent Assault',
        'kidnap': 'Missing Person',
        'robbery': 'Robbery',
        'autotheft': 'Auto Theft',
        'larceny': 'Larceny',
        'burglary': 'Burglary',
        'conduct': 'Disorderly Conduct',
        'disputes': 'Verbal Disputes',
        'prostitution': 'Prostitution',
        'sexoffender': 'Sex Offender'
    }

    final_crime_array = []
    #Get data from database
    all_crimes = CrimeDataPoint.objects.all()

    for (key, value) in filters.items():
        name = request.GET.get(key, False)
        if name:
            final_crime_array.extend(all_crimes.filter(offense_code_group__icontains=value))

    #Get locations of start and end
    locA = geocoder.google(location_a)
    locB = geocoder.google(location_b)
    latlongA = locA.latlng
    latlongB = locB.latlng
    print(latlongA, latlongB)

    #Create Ellipse from start and end location
    ell = Ellipse.Ellipse(latlongA[0], latlongA[1], latlongB[0], latlongB[1])
    jsonObject = []
    for crime in final_crime_array:
        #If the crime has a longitude and latitude

        if not (crime.latitude or crime.longitude):
            continue
        #If the crime is within the ellipse
        print(ell.isWithinEllipse(crime.latitude, crime.longitude))
        if ell.isWithinEllipse(crime.latitude, crime.longitude):
            #Add to the json object
            json_entry = {
                'lat': crime.latitude,
                'lng': crime.longitude,
                'weight': 5,
                'radius': 0.5,
            }
            print(json_entry)
            jsonObject.append(json_entry)
    print(jsonObject)

    #Send to MapQuest API
    map_quest_api = Send_Data(latlongA, latlongB, jsonObject)

    #Try getting route directions
    try:
        route = map_quest_api.Get_Directions()['route']['legs'][0]['maneuvers']
        mapquest_waypts = json.dumps([maneuver['startPoint'] for maneuver in route][1:-1])
    except:
        return redirect('/')


    context = {
        'location_a': location_a,
        'location_b': location_b,
        'route': route,
        'mapquest_waypts': mapquest_waypts,
        'googleAPI': GoogleMaps_API,
        'googleJS_API': Google_JS_API,
        'jsonObject': jsonObject,
    }
    # This renders our the crime-map.html file with all of the defined context
    # variables
    return render(request, 'pages/crime-map.html', context)
