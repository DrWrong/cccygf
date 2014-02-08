from urllib.request import urlopen
from urllib.parse import urlencode,quote_plus
import json,hmac
from datetime import datetime
from hashlib import sha1
from base64 import b64encode
from django.core.urlresolvers import reverse
from cccygf.settings import HOST

app_id='202463130000034602'
app_secret='74045aa7fc22d81e934ac35e6f2d788a'

def get_access_token():
	grant_type='client_credentials'
	postdata={'grant_type':grant_type,
			'app_id':app_id,
			'app_secret':app_secret}
	postdata=urlencode(postdata).encode('utf-8')
	urlhandler=urlopen('https://oauth.api.189.cn/emp/oauth2/v2/access_token',data=postdata)
	data=urlhandler.readall().decode('utf-8')
	data=json.loads(data)
	return data['access_token']

def create_sign(args):
	encodeargs=args.encode('utf-8')
	hmacobj=hmac.new(app_secret.encode('utf-8'),encodeargs,sha1)
	sign=hmacobj.digest()
	sign=b64encode(sign).decode('utf-8')
	sign=quote_plus(sign)
	return sign

def get_auth_token():
	access_token=get_access_token()
	timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	args=['app_id='+app_id,'access_token='+access_token,
	'timestamp='+timestamp]
	args.sort()
	args='&'.join(args)
	args+=('&sign='+create_sign(args))
	url='http://api.189.cn/v2/dm/randcode/token?'+args
	urlhandler=urlopen(url)
	data=urlhandler.readall().decode('utf-8')
	data=json.loads(data)
	return data['token']

def send_verify_message(phone):
	url=reverse('validate:callback')
	url='http://'+HOST+url
	data=['app_id='+app_id,
		'access_token='+get_access_token(),
		'token='+get_auth_token(),
		'phone='+phone,
		'url='+url,
		'timestamp='+datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		]
	data.sort()
	postdata='&'.join(data)
	postdata+=('&sign='+create_sign(postdata))
	print(postdata)
	postdata=postdata.encode('utf-8')
	urlhandler=urlopen('http://api.189.cn/v2/dm/randcode/send',data=postdata)
	data=urlhandler.readall().decode('utf-8')
	data=json.loads(data)
	return data