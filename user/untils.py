from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import hashlib
from django.core.mail import send_mail
from base64 import urlsafe_b64encode
from string import Template
import hmac
from cccygf.settings import HOST
import re
from captcha.models import CaptchaStore, get_safe_now
from validate.models import MoblieVerifyCode,get_latest
def randomstr(seed):
	time=timezone.now().timestamp()
	origstr=str(time)+seed
	origstr=origstr.encode()
	m=hashlib.md5()
	m.update(origstr)
	randstr=m.hexdigest()
	return randstr
def hash_sign(msg):
	key=b'CcCyGf_Toge2Ther'
	msg=msg.encode('utf8')
	hmacobj=hmac.new(key,msg=msg)
	hashmsg=hmacobj.digest()
	hashmsg=urlsafe_b64encode(hashmsg).decode('utf8')
	return hashmsg

def autousername():
	time=timezone.now().timestamp()
	username='u'+str(time)
	return username
def finalusername():
	while 1:
		username=autousername()
		try:
			User.objects.get(username)
		except ObjectDoesNotExist:
			break
	return username
def sendmail(email,hash_url,username):
	
	username=username.encode('utf8')
	url='http://'+HOST+'/'+hash_url+'/'+urlsafe_b64encode(username).decode('uft8')
	message=Template('''
尊敬的用户:
	欢迎加入CC创意工坊，请您使用以下链接激活你的CC账户 $url 。
	如有任何问题请联系客服电话：13718394905

	CC文化团队''')
	send_mail('【cc创意工坊】请激活你的账户',message.safe_substitute({'url':url}),'creativeculture1@163.com',[email])

def email_legal(email):
	if re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-z0-9_-])+$',email):
		return True
	else:
		return False

def verifycode_correct(key,response):
	response=response.lower()
	CaptchaStore.remove_expired()
	try:
		CaptchaStore.objects.get(response=response,hashkey=key,expiration__gte=get_safe_now()).delete()
	except CaptchaStore.DoesNotExist:
		return False
	return True	

def mobilecode_correct(mobile,response):
	MoblieVerifyCode.remove_expired()
	try:
		MoblieVerifyCode.objects.get(mobile=mobile,verifycode=response,create_at__gte=get_latest()).delete()
	except ObjectDoesNotExist:
		return False
	return True