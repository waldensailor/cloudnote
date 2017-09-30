from django.contrib import admin

# Register your models here.

from main_view import models
admin.site.register(models.Article)
admin.site.register(models.Tag)