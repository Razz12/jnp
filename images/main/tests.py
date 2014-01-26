from django.test import TestCase
from django.utils import unittest
from main.models import Image
from django.db import connections

class ImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image1 = Image.objects.create(title = "Piekne zdjecie", tags = ["aa","bb"],description = "hyhy hue hue")
        self.image2 = Image.objects.create(title = "Niepiekne zdjecie", tags = ["aa","bb"],description = "hyhy hue hue")
        self.image1.save()
        self.image2.save()
        database_wrapper = connections['default']
        col = database_wrapper.get_collection('main_images')
        col.create_index( { "tags": "text", "title": "text", "description": "text" } )
        
    def testSpeaking(self):
        self.assertEqual("OK", "OK")
        ret = self.image1.full_text("e");
        #ret = Image.objects.all()
        print("Results")
        for e in ret:
            print(e.title)
