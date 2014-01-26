from django.utils import timezone

import hashlib

def randomstr(seed):
	time=timezone.now().timestamp()
	origstr=str(time)+seed
	origstr=origstr.encode()
	m=hashlib.md5()
	m.update(origstr)
	randstr=m.hexdigest()
	return randstr




