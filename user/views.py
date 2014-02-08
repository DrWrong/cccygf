from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from validate.models import MoblieVerifyCode,ValidateCode
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from user.untils import finalusername,hash_sign,sendmail
from django.contrib.auth.models import User
from user.models import UserInfo
from base64 import urlsafe_b64decode

# Create your views here.
@ensure_csrf_cookie
def register(request):
	return render(request,'user/register.html',{})

def register_mobile(request):
	if request.method=='POST':
		req=json.load(request.body)
		mobile=req['mobile']
		verifycode=req['verifycode']
		password=req['password']
		confirmpass=req['confirmpass']
		useragreement=req['useragreement']
		data={}
		if not useragreement:
			data['status']=13
			data['error']='必须同意用户协议才能注册'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		try:
			entry=MoblieVerifyCode.objects.get(mobile=mobile)
		except ObjectDoesNotExist:
			data['status']=8
			data['error']='手机号码未经过验证'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		if entry.verifycode!=verifycode:
			data['status']=9
			data['error']='验证码不正确'
			entry.delete()
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		entry.delete()
		if password!=confirmpass:
			data['status']=10
			data['error']='密码前后不一致'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		password=make_password(password)
		username=finalusername()
		user=User(username=username,password=password,is_staff=False,is_active=True,is_superuser=False)
		user.save()
		user=User.objects.get(username)
		userinfo=UserInfo(user=user,mobile=mobile)
		userinfo.save()
		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
	return HttpResponse(status=400)

def register_email(request):
	if request.method=='POST':
		req=json.load(request.body)
		email=req['email']
		password=req['passwrod']
		confirmpass=req['confirmpass']
		verifycode=req['verifycode']
		useragreement=req['useragreement']
		data={}
		if not useragreement:
			data['status']=13
			data['error']='必须同意用户协议才能注册'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		try:
			entry=ValidateCode.objects.get(session=request.session.session_key)
		except ObjectDoesNotExist:
			data['status']=11
			data['error']='内部错误'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		if entry.validatestr!=verifycode:
			data['status']=9
			data['error']='验证码不正确'
			entry.delete()
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		entry.delete()
		if password!=confirmpass:
			data['status']=10
			data['error']='密码前后不一致'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		password=make_password(password)
		user=User.objects.filter(email=email)
		if len(user)!=0:
			data['status']=12
			data['error']='邮箱已注册'
			return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
		username=finalusername()
		user=User(username=username,password=password,email=email,\
			is_staff=False,is_active=False,is_superuser=False)
		user.save()
		hash_url=hash_sign(username)
		sendmail(email,hash_url,username)
		data['status']=0
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
	else:
		return HttpResponse(status=400)

def active_email(request,sign,usernamehash):
	usernamehash=usernamehash.encode('utf8')
	username=urlsafe_b64decode(usernamehash).decode('utf8')
	if sign!=hash_sign(username):
		return render(request,'user/active.html',{'message':'非法的链接'})
	try:
		user=User.objects.get(username=username)
	except ObjectDoesNotExist:
		return render(request,'user/active.html',{'message':'非法的链接'})
	user.is_active=True
	user.save()
	return render(request,'user/active.html',{'message':'用户已激活'})

def useragreement(request):
	return render(request,'user/useragreement.html',{})