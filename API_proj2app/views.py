# standard imports

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse, QueryDict
from django.urls import include, path
from rest_framework import routers
from API_proj2app.models import *

# Create your views here.

class index(View):
    def login(request):
        # Only POST
        request.session["session_name"] = #set this to the username #learned sessions from session documentation: https://docs.djangoproject.com/en/2.2/topics/http/sessions/

    def newUser(request):
        # Only POST

    # handle all requests at memories
    def handleMemories(request):
        session_name = request.session["session_name"]

        if request.method == "GET":

        if request.method == "POST":

        if request.method == "PATCH":

        if request.method == "DELETE":

class userInfo(View):

    # handles only GET requests
    def aoi(request, user_id):
        return JsonResponse(userInfo.getAllLocations(request,user_id))

    def getAllLocations(request,user_id):
        data = {}
        usr = User.objects.get(id=user_id)

        # The user's latitude and longitude can be unset, so we have to account for that
        lat = None
        lon = None
        if usr.latitude != None:
            lat = float(usr.latitude)
        if usr.longitude != None:
            lon = float(usr.longitude)

        data['Homebase'] = (lat, lon) # adds the homebase to the list
        for location in Location.objects.filter(userID=user_id):
            # creates a list of all the user's locations
            data[location.place_title] = (float(location.latitude), float(location.longitude))

        return data # returns a dictionary so it can be used multiple times


    # handles only GET and POST requests
    def users(request):
        # request.method code from https://docs.djangoproject.com/en/2.2/topics/db/queries/
        if request.method == "GET":
            data = {}
            for usr in User.objects.all():
                # fairly straightforward loop to display all users
                data[usr.id] = str(usr.display_name) + " (@" + str(usr.username) + ")"
            return JsonResponse(data)
        elif request.method == "POST":
            # QueryDict from https://docs.djangoproject.com/en/2.2/topics/db/queries/
            data = QueryDict(request.META["QUERY_STRING"]).dict()
            User.objects.create(display_name=data["display_name"],
                                username=data["username"],
                                longitude=data["longitude"],
                                latitude=data["latitude"])
            response = {"Message":"OK (200)"}
        else:
            response = {"Message":"WRONG REQUEST (400)"}
        return JsonResponse(response)

    # the following two methods were created to reduce redundancies in modifying obujects
    def modifyUser(request, user_id):
        return userInfo.modify(request, User.objects.get(id=user_id))

    def modifyLocation(request, user_id, placeTitle):
        return userInfo.modify(request, Location.objects.get(userID=user_id, place_title = placeTitle))

    # handles only PATCH and DELETE requests
    def modify(request, obj):
        if request.method == "PATCH":
            data = QueryDict(request.META["QUERY_STRING"]).dict()
            # following loop from https://stackoverflow.com/questions/1576664/how-to-update-multiple-fields-of-a-django-model-instance
            for (key, value) in data.items():
                setattr(obj, key, value)
            obj.save()
            response = {"Message":"UPDATED (200)"}
        elif request.method == "DELETE":
            obj.delete()
            response = {"Message":"DELETED (200)"}
        else:
            response = {"Message":"WRONG REQUEST (400)"}
        return JsonResponse(response)

    # handles only GET and POST requests
    def locations(request):
        # this method follows the structure of users() above
        if request.method == "GET":
            data = {}
            for usr in User.objects.all():
                data[str(usr.username) + " (id: " + str(usr.id) + ")"] = userInfo.getAllLocations(request,usr.id)
            return JsonResponse(data)
        if request.method == "POST":
            data = QueryDict(request.META["QUERY_STRING"]).dict()
            Location.objects.create(userID=data["id"],
                                    place_title=data["place_title"],
                                    address=data["address"],
                                    city=data["city"],
                                    state=data["state"],
                                    zip_code = data["zip_code"])
            response = {"Message":"OK (200)"}
            return JsonResponse(response)
