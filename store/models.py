from django.db import models
from django.contrib.auth.models import User
# Create your models here
#商品详情
class Products(models.Model):
	"""docstring for Products
	   this is products table"""
	name=models.CharField(max_length=50)
	price=models.FloatField()
	#不同规格的相同产品
	productgroup=models.ForeignKey(ProductsGroup)
	#相同产品的显著差别
	feature=models.CharField(max_length=30)
	def __str__(self):
		self.name

# 商品的规格参数名-值对
class Parameter(models.Model):
	"""docstring for Parameter"""
	product=models.ForeignKey(Products)
	name=models.CharField(max_length=50)
	value=models.CharField(max_length=100)

#每件商品的展示图
class ProductImage(models.Model):
	"""docstring for ProductImage
	table to restore image url for product"""
	product=models.ForeignKey(Products)
	image=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/%s/%s'%(instance.product.productgroup.merchant.name,\
			instance.product.productgroup.category,instance.product.productgroup.name,\
			instance.product.name,filename)))

#同类商品组
class ProductsGroup(models.Model):
	name=models.CharField(max_length=50)
	merchant=models.ForeignKey(User)
	category=models.CharField(max_length=50)
	#首页显示图片
	indeximage=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/indeximage.png'%(instance.merchant.name,\
			instance.category,instance.name)),blank=True)
	#分类页显示图片
	categoryimage=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/categoryimage.png'%(instance.merchant.name,\
		instance.category,instance.name)),blank=True)
	#产品上线时间
	pubtime=models.DateField(auto_now_add=True,'product online time')	
	video=models.URLField(blank=True,'use video in other website')
#过滤选项
class FilterChoice(models.Model):
	productgroup=models.ForeignKey(ProductsGroup)
	name=models.CharField(max_length=50)
	value=models.CharField(max_length=50) 
#商品详情展示资料如图片
class ProductDetailImage(models.Model):
	"""docstring for ProductDetailImage 
	展示商品图片信息"""
	productgroup=models.ForeignKey(ProductsGroup)
	image=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/deailimage/%s'\
		%(instance.productgroup.merchant.name,
			instance.productgroup.category,
			instabce.productgroup.name,filename)))
#商品评论表
class Comment(models.Model):
	"""docstring for Comment"""
	productgroup=models.ForeignKey(ProductsGroup)
	user=models.ForeignKey(User)
	content=models.TextField()
	#客服回应
	staff_respond=models.TextField()
	#用户评分
	score=models.PostiveSmallIntegerField(default=5)
	date=models.DateField(auto_now_add=True)
	useful=models.PostiveSmallIntegerField(default=0)

	def is_score_legal(self):
		if self.score<=5:
			return True
		return False

#用户商家信息表
class UserInfo(models.Model):
	"""docstring for Merchant"""
	user=models.OneToOneField(User)
	mobile=models.CharField(max_length=11)
	

