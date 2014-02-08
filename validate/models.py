from django.db import models
from datetime import datetime,timedelta
# Create your models here.
class ValidateCode(models.Model):
	session=models.CharField(blank=True,max_length=100,unique=True)
	validatestr=models.CharField(max_length=4)
	validateimg=models.ImageField(upload_to='validateimg')


class MoblieVerifyCode(models.Model):
	mobile=models.CharField(max_length=11,unique=True)
	verifycode=models.CharField(max_length=6,blank=True)
	creat_at=models.DateTimeField()
	identifier=models.CharField(max_length=4,unique=True)
	def code_effective(self):
		if datetime.now()<self.creat_at+timedelta(minutes=2):
			return True
		self.delete()
		return False