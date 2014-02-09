import json
from validate.untils import send_verify_message,mobile_legal
from validate.models import MoblieVerifyCode
from user.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.http import HttpResponse
from user.untils import hash_sign
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
# Create your views here.
def smssend(request):
	if request.method=='POST':
		req=json.loads(request.body)
		try:
			mobile=req['moblie']
		except KeyError:
			status=14
			error='缺少必要的项'
		else:
			if not mobile_legal(mobile):
				status=15
				error='手机号码不合法'
			else:
				try:
					UserInfo.object.get(moblie=mobile)
				except ObjectDoesNotExist:
					data=send_verify_message(mobile)
					mobilecode=MoblieVerifyCode.objects.get_or_create(moblie=mobile)
					mobilecode.identifier=data['identifier']
					mobilecode.create_at=datetime.fromtimestamp(data['create_at'])
					mobilecode.save()
					status=0
					error=''
				else:
					status=16
					error='手机已注册'
		data=dict(status=status,error=error)
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
	return HttpResponse(status=400)
def callback(request,sign):
	if request.method=='POST':
		try:
			rand_code=request.POST['rand_code']
			identifier=request.POST('identifier')
		except KeyError:
			data=dict(res_code='1')
		else:
			try:
				mobilecode=MoblieVerifyCode.objects.get(identifier=identifier)
			except ObjectDoesNotExist:
				data=dict(res_code='1')
			else:
				if hash_sign(mobilecode.mobile)==sign:
					mobilecode.verifycode=rand_code
					data=dict(res_code='0')
				else:
					data=dict(res_code='1')
		return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')
	return HttpResponse(status=400)

def create_validatecode(request):
	data=dict()
	data['cptch_key']=CaptchaStore.generate_key()
	data['cptch_image']=captcha_image_url(data['cptch_key'])
	return HttpResponse(json.dumps(data),content_type='application/json')

