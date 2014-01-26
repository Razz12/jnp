from django.db import models, connections
from djangotoolbox.fields import ListField
from django_mongodb_engine.storage import GridFSStorage
from django_mongodb_engine.contrib import MongoDBManager

from string import join
import os
from PIL import Image as PImage
from images.settings import MEDIA_ROOT

from .forms import StringListField

media_storage = GridFSStorage(location='/media');

class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)



class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/", storage = media_storage, null = True)#remove null = True
    tags = CategoryField()
    description = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.image.name
        
    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        #needs to read from somewhere else
        #im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        #self.width, self.height = im.size
        #super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    def thumbnail(self):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="40" /></a>""" % (
                                                                 (self.image.name, self.image.name))
    @staticmethod
    def from_mongo(doc):
		return Image.objects.create(title = doc.get('title'), image = doc.get('image'), tags = doc.get('tags'),
			description = doc.get('description'), created = doc.get('created'), rating = doc.get('rating'),
			width = doc.get('width'), height = doc.get('height'))
     
    @staticmethod
    def full_text(search_text):
		database_wrapper = connections['default']
		db = database_wrapper.database
		ret = []
		mongolist = db.command(
			"text",
			"main_image",
			search="kupka")['results']
		for mongos in mongolist:
			print("Mam mongosa: " + str(mongos))
			ret.append(Image.from_mongo(mongos['obj']))
		return ret
    
    thumbnail.allow_tags = True
    objects = MongoDBManager()

	
