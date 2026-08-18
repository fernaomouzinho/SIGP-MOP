import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_ver(instance, filename):
	upload_to = 'ver/{}/'.format(instance.eval.id)
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}.{}'.format(instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_versec(instance, filename):
	upload_to = 'ver/{}/'.format(instance.ver.eval.id)
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}.{}'.format(instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
