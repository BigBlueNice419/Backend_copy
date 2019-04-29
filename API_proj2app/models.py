from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import User
import urllib
import json
# helpful link: https://www.digitalocean.com/community/tutorials/how-to-create-django-models
# The User model. The user_id is automatically generated
class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    # for displaying a user objects
    def __str__(self):
        return self.username + " (name: " + str(self.firstname) + " " + str(self.lastname) + ")"

class Post(models.Model):
    userID = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/') # allows users to upload images: https://wsvincent.com/django-image-uploads/
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
             return "title: " + str(self.title) + " date: " + str(self.date) + " (id:" + str(self.userID) + ")"

    class Meta:
        ordering = ['created_on']

        def __unicode__(self):
            return self.title

# The Location model
# class Location(models.Model):
#     userID = models.CharField(max_length=20, null=True)
#     place_title = models.CharField(max_length=50)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=2)
#     zip_code = models.CharField(max_length=5, null=True)
#     # latitude and longitude are not editable and cannot be seen by the user
#     latitude = models.DecimalField(max_digits=18, decimal_places=10, null=True, editable=False)
#     longitude = models.DecimalField(max_digits=18, decimal_places=10, null=True, editable=False)
#
#     #for displaying a location object
#     def __str__(self):
#         return "title: " + str(self.place_title) + " (id:" + str(self.userID) + ")"
#
#     # overwrites the default save method so that the calculated latitude and longitude are added
#     # args and kwargs had to be added to fix "force_insert" error when POSTing
#     def save(self, *args, **kwargs):
#         # creating a location string that is the full address for the poi
#         # which is then used by geocode to calculate the latitude and longitude
#         location = "%s, %s, %s %s" % (self.address, self.city, self.state, self.zip_code)
#         self.latitude, self.longitude = self.geocode(location)
#         super(Location, self).save()
#
#     # calculates latitude and longitude based on the full address of the poi
#     # helpful links:
#     # https://stackoverflow.com/questions/2755027/geocoding-an-address-on-form-submission
#     # https://developers.google.com/maps/documentation/geocoding/intro
#     def geocode(self, location):
#         # creating a google maps api request
#         location = urllib.parse.quote_plus(location)
#         request = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (location, settings.GOOGLE_API_KEY)
#         response = urllib.request.urlopen(request)
#         data = json.loads(response.read().decode('utf8'))
#
#         if data['status'] == 'OK':
#             lat = data['results'][0]['geometry']['location']['lat']
#             lng = data['results'][0]['geometry']['location']['lng']
#
#             return Decimal(lat), Decimal(lng)
