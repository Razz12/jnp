from django.shortcuts import render
from main.models import Image
from django.db import connections
from django.http import HttpResponse,HttpResponseNotFound
from django_mongodb_engine.storage import GridFSStorage
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files import File

def rawImageView(request, imagename):
	media_storage = GridFSStorage(location='/media/images/')
	try:
		file = media_storage.open(imagename, "rb")
		return HttpResponse(file.read(), mimetype="image/png")
	except:
		return HttpResponse('', mimetype="image/png")

@csrf_exempt
def postImageView(request):
	print("IN\n");
	data=json.loads( request.raw_post_data )
	#print("HY " + data['image'] + "\n")
	image = base64.b64decode(data['image'])
	f = open("/home/razz/image.png", "wb+")
	f.write(image)
	f.close()
	f = open("/home/razz/image.png", "rb")
	print("KUPACZ\n")
	data['image']=File(f)
	doc = data
	#print("OKI1\n");
	imageModel = Image.objects.create(title = doc.get('title'),image = File(f),tags = doc.get('tags'),
			description = doc.get('description'))
	s = doc.get('title')
	#print("he\n")
	###name = "".join(c.lower() for c in s if not c.isspace())
	#print("SAVING TO " + name)
	#imageModel.image.save(name, File(f))
	

	print("OKI\n");
	return HttpResponse("{'OK':1}", mimetype="application/json")
