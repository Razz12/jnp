from django.contrib import admin
from models import Tag, Image


# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "rating", "size",
        "thumbnail", "created"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
