from django.db import models, connections
from djangotoolbox.fields import ListField
from django_mongodb_engine.storage import GridFSStorage
from django_mongodb_engine.contrib import MongoDBManager
#from django_mongodb_engine import ImageField

from string import join
import os
from PIL import Image as PImage
from images.settings import MEDIA_ROOT

from .forms import StringListField

media_storage = GridFSStorage(location='/media/images/');

class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)



class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="/", storage = media_storage, null = True)#remove null = True
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
        f = media_storage.open(self.image.name, "rb")
        im = PImage.open(f)
        self.width, self.height = im.size
        f.close()
        super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    def thumbnail(self):
        return """<a href="/media%s"><img border="0" alt="" src="/media%s" height="40" /></a>""" % (
                                                                 (self.image.name, self.image.name))
    def toDict(self):
		ret = { }
		ret["title"]=self.title
		ret["image"]=self.image.name
		ret["tags"]=self.tags
		ret["description"]=self.description
		#ret["created"]=self.created
		#ret["rating"]=self.rating
		#ret["width"]=self.width
		#ret["height"]=self.height
		return ret
    @staticmethod
    def from_mongo_to_dict(doc):
		ret = { }
		ret["title"]=doc.get('title')
		ret["image"]=doc.get('image')
		ret["tags"]=doc.get('tags')
		ret["description"]=doc.get('description')
		ret["created"]=str(doc.get('created'))
		ret["rating"]=doc.get('rating')
		ret["width"]=doc.get('width')
		ret["height"]=doc.get('height')
		return ret
     
    @staticmethod
    def full_text(search_text):
		database_wrapper = connections['default']
		db = database_wrapper.database
		ret = []
		mongolist = db.command(
			"text",
			"main_image",
			search=search_text)['results']
		for mongos in mongolist:
			print("Mam mongosa: " + str(mongos))
			ret.append(Image.from_mongo_to_dict(mongos['obj']))
			print("POSZLO")
		return ret
    
    thumbnail.allow_tags = True
    objects = MongoDBManager()

	
