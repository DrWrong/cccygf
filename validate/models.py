from django.db import models
from datetime import datetime,timedelta
# Create your models here.
def get_latest():
	return datetime.now()-timedelta(minutes=2)

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
	def remove_expired(cls):
		cls.objects.filter(create_at__lte=get_latest()).delete()
	remove_expired=classmethod(remove_expired)