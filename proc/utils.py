import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_proc(instance, filename):
	upload_to = 'proc/{}/'.format(instance.proc.proj.id)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_procfiles(instance, filename):
	upload_to = 'proc/{}/'.format(instance.proc.proj.id)
	field = 'files'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
