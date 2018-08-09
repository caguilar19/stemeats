from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Cuisine)
admin.site.register(Restaurant)
admin.site.register(Post)
admin.site.register(Comment)