import json
from validate.untils import send_verify_message,
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
			if not 

def callback(request):
	pass

		


