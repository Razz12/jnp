from django.contrib import admin
from models import Tag, Image


# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "rating", "size", "tags_",
        "thumbnail", "created"]
    list_filter = ["tags", ]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
