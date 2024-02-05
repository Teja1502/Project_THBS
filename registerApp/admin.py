# myapp/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Readlist)
admin.site.register(Favourites)
admin.site.register(UserProfile)
admin.site.register(Profile)
