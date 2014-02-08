from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here
#商品详情
class Products(models.Model):
	"""docstring for Products
	   this is products table"""
	name=models.CharField(max_length=50)
	#库存量
	amount=models.PositiveSmallIntegerField()

	#不同规格的相同产品
	productgroup=models.ForeignKey('ProductsGroup')
	#相同产品的显著差别
	feature=models.CharField(max_length=30)
	#产品小图
	sketch=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/%s/'%(instance.productgroup.merchant.name,\
			instance.productgroup.category.name,instance.productgroup.name,\
			instance.name)))
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
		'productimage/%s/%s/%s/%s/'%(instance.product.productgroup.merchant.name,\
			instance.product.productgroup.category.name,instance.product.productgroup.name,\
			instance.product.name)))

#同类商品组
class ProductsGroup(models.Model):
	name=models.CharField(max_length=50)
	merchant=models.ForeignKey('Merchant')
	category=models.ForeignKey('Category')
	price=models.FloatField()
	saleprice=models.FloatField(blank=True,null=True)
	issale=models.BooleanField(default=False)
	vipprice=models.FloatField()
	cost=models.FloatField()
	#商品是否在线
	active=models.BooleanField(default=False)
	#首页显示图片
	indeximage=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/indeximage.png'%(instance.merchant.name,\
			instance.category.name,instance.name)),blank=True)
	#分类页显示图片
	categoryimage=models.ImageField(upload_to=(lambda instance,filename:\
		'productimage/%s/%s/%s/categoryimage.png'%(instance.merchant.name,\
		instance.category.name,instance.name)),blank=True)
	#产品上线时间
	pubtime=models.DateField('product online time',auto_now_add=True)
	video=models.URLField('use video in other website',blank=True)
	salenumber=models.PositiveSmallIntegerField(default=0)
	commentnumber=models.PositiveSmallIntegerField(default=0)
	hitnumber=models.PositiveSmallIntegerField(default=0)
	recommand=models.BooleanField(default=False)
	def save(self,*args,**kwargs):
		if self.issale==True:
			if self.saleprice==None:
				raise ValidationError('促销产品未填写促销价格')

#同类产品推荐
class RecommandProducts(models.Model):
	"""docstring for RecommandProducts"""
	srcproduct=models.ForeignKey(ProductsGroup)
	recpid=models.PositiveSmallIntegerField()
#分类
class Category(models.Model):
	"""docstring for Category"""
	name=models.CharField(max_length=50)
	#所属组 方便后续产品扩大时添加
	small_products=models.BooleanField(default=False)


#过滤选项
class FilterChoice(models.Model):
	productgroup=models.ManyToManyField(ProductsGroup)
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
			instance.productgroup.name,filename)))
#商品评论表
class Comment(models.Model):
	"""docstring for Comment"""
	productgroup=models.ForeignKey(ProductsGroup)
	user=models.ForeignKey(User)
	content=models.TextField()
	#客服回应
	staff_respond=models.TextField()
	#用户评分
	score=models.PositiveSmallIntegerField(default=5,validators=[MaxValueValidator(5)])
	date=models.DateField(auto_now_add=True)
	useful=models.PositiveSmallIntegerField(default=0)

#	def save(self,*args,**kwargs):
#		if self.score>=5:
#			raise Exception("comment score shoud under 5")
#		else:
#			super(Comment,self).save(*args,**kwargs)
#			productgroup=self.productgroup
#			productgroup.commentnumber+=1
#			productgroup.save()





