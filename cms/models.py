from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Flash(models.Model):
	"""docstring for Flash"""
	flash=models.FileField(uploadto='leadingflash')

class Gallery(models.Model):
	"""docstring for Gallery"""
	img=models.ImageField(uploadto='gallery/')
	targeturl=models.URLField()
	def auto_create_url(self,pid):
		self.targeturl=reverse('store:detail',args=[pid])