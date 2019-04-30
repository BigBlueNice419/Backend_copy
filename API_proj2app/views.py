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
        request.session["session_name"] = User.objects.get(username)#set this to the username #learned sessions from session documentation: https://docs.djangoproject.com/en/2.2/topics/http/sessions/

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
        return JsonResponse(userInfo.getAllInfo(request,user_id))

    def getAllInfo(request,user_id):
        data = {}
        usr = User.objects.get(id=user_id)

        for memory in Memory.objects.filter(userID=user_id):
            # creates a list of all the user's memory/note titles
            data[memory.title, memory.content, memory.image, memory.date] = (str(urs.title) + str(usr.content) + str(usr.image) + str(usr.date))

        return data # returns a dictionary so it can be used multiple times


    # handles only GET requests
    # def aoi(request, user_id):
    #     return JsonResponse(userInfo.getAllLocations(request,user_id))
    #
    # def getAllLocations(request,user_id):
    #     data = {}
    #     usr = User.objects.get(id=user_id)
    #
    #     # The user's latitude and longitude can be unset, so we have to account for that
    #     lat = None
    #     lon = None
    #     if usr.latitude != None:
    #         lat = float(usr.latitude)
    #     if usr.longitude != None:
    #         lon = float(usr.longitude)
    #
    #     data['Homebase'] = (lat, lon) # adds the homebase to the list
    #     for location in Location.objects.filter(userID=user_id):
    #         # creates a list of all the user's locations
    #         data[location.place_title] = (float(location.latitude), float(location.longitude))
    #
    #     return data # returns a dictionary so it can be used multiple times


    # handles only GET and POST requests
    def users(request):
        # request.method code from https://docs.djangoproject.com/en/2.2/topics/db/queries/
        if request.method == "GET":
            data = {}
            for usr in User.objects.all():
                # fairly straightforward loop to display all users
                data[usr.id] = str(usr.firstname) + " " + str(usr.lastname) + " (@" + str(usr.username) + ") " + " " + str(usr.password) "
            return JsonResponse(data)
        elif request.method == "POST":
            # QueryDict from https://docs.djangoproject.com/en/2.2/topics/db/queries/
            data = QueryDict(request.META["QUERY_STRING"]).dict()
            User.objects.create(firstname=data["firstname"],
                                lastname=data["lastname"],
                                username=data["username"],
                                password=data["password"])
            response = {"Message":"OK (200)"}
        else:
            response = {"Message":"WRONG REQUEST (400)"}
        return JsonResponse(response)

    # the following two methods were created to reduce redundancies in modifying obujects
    def modifyUser(request, user_id):
        return userInfo.modify(request, User.objects.get(id=user_id))

    def modifyTitle(request, user_id, title):
        return userInfo.modify(request, Memory.objects.get(userID=user_id, title = title))

    def modifyContent(request, user_id, content):
        return userInfo.modify(request, Memory.objects.get(userID=user_id, content = content))

    def modifyImage(request, user_id, image):
        return userInfo.modify(request, Memory.objects.get(userID=user_id, image = image))

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
    def memories(request):
        # this method follows the structure of users() above
        if request.method == "GET":
            data = {}
            for usr in User.objects.all():
                data[str(usr.username) + " (id: " + str(usr.id) + ")"] = userInfo.getAllInfo(request,usr.id)
            return JsonResponse(data)
        if request.method == "POST":
            data = QueryDict(request.META["QUERY_STRING"]).dict()
            Memory.objects.create(userID=data["id"],
                                    title=data["title"],
                                    content=data["content"],
                                    image=data["image"],
                                    date=data["date"])
            response = {"Message":"OK (200)"}
            return JsonResponse(response)
