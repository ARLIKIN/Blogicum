from django.contrib import admin
from .models import Category, Location, Post


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Location)