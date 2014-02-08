from django.db import models
from django.contrib.auth.models import User
from user.untils import randomstr


# Create your models here.
#用户信息表
class UserInfo(models.Model):
	"""docstring for Merchant"""
	user=models.OneToOneField(User)
	mobile=models.CharField(max_length=11,blank=True)
	score=models.PositiveSmallIntegerField()
	vip=models.BooleanField(default=False)
	sina_uid=models.CharField(max_length=20,blank=True,unique=True)
	renren_token=models.CharField(max_length=20,blank=True,unique=True)
	qq_token=models.CharField(max_length=20,blank=True,unique=True)

#商户信息
class Merchant(UserInfo):
	"""docstring for Merchant"""
	name=models.CharField("公司名称",max_length=20)
	identify_number=models.CharField(max_length=18)
	identify_card=models.ImageField(upload_to=(lambda instance,filename:\
		'merchantimage/%s/id_card/%s/%s'%(instance.name,randomstr())))



#用户地址
class Address(models.Model):
	user=models.ForeignKey(User)
	recipient=models.CharField(max_length=50)
	#用户地区　由前端生成有效字符串
	district=models.CharField(max_length=100)
	#用户详细地址
	address=models.CharField(max_length=100)
	mobile=models.CharField(max_length=11)
	telphone=models.CharField(max_length=12,blank=True)
	mail=models.EmailField()
	current_use=models.BooleanField(default=True)

#发票表
class invoice(models.Model):
	"""docstring for invoice"""
	user=models.ForeignKey(User)
	tittle=models.CharField(max_length=100)
	content_choice=(
		('明细','明细'),
		('办公用品','办公用品'),
		('电脑配件','电脑配件'),
		('耗材','耗材'))
	content=models.CharField(max_length=10)
	content_use=models.BooleanField(default=True)
