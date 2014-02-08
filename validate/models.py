from django.db import models

# Create your models here.
class ValidateCode(models.Model):
	session=models.CharField(blank=True,max_length=100,unique=True)
	validatestr=models.CharField(max_length=4)
	validateimg=models.ImageField(upload_to='validateimg')


class MoblieVerifyCode(models.Model):
	mobile=models.CharField(max_length=11,unique=True)
	verifycode=models.CharField(max_length=8)
