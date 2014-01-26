from django.shortcuts import render
from main.models import Image
from django.db import connections
from django.http import HttpResponseNotFound

def fullTextView(self):
	#self.image1 = Image.objects.create(title = "Piekne zdjecie", tags = ["aa","bb"],description = "hyhy hue hue")
	#self.image2 = Image.objects.create(title = "Niepiekne zdjecie", tags = ["aa","bb"],description = "hyhy hue hue")
	#self.image1.save()
	#self.image2.save()
	#for con in connections:
	#	print(con)
	#database_wrapper = connections['default']
	#col = database_wrapper.get_collection('main_images')
	#col.ensure_index( { "tags": "text", "title": "text", "description": "text" } )
	ret = Image.full_text("Piekne")
	#ret = Image.objects.all()
	print("Results")
	for im in ret:
		print(im)
	print("ENDOfresults");
	return HttpResponseNotFound('<h1>Page not found</h1>')
