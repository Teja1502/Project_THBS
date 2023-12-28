# myapp/admin.py
from django.contrib import admin
from .models import Readlist, Favourites, UserProfile

admin.site.register(Readlist)
admin.site.register(Favourites)
admin.site.register(UserProfile)
