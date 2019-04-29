from django.contrib import admin
from SQLapp.models import *
# Imports and registers the Location and User models
admin.site.register(User)
admin.site.register(Location)
