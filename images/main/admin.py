from django.contrib import admin
from models import Image

def tags(instance):
    return ', '.join(instance.tags)

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "rating", "size", tags,
        "thumbnail", "created"]

admin.site.register(Image, ImageAdmin)
