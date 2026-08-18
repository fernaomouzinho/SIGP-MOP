import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_inv(instance, filename):
	upload_to = 'finance/inv/{}/'.format(instance.project.id)
	field = 'inv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cert(instance, filename):
	upload_to = 'finance/cert/{}/'.format(instance.contract.project.id)
	field = 'cert'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_recom(instance, filename):
	upload_to = 'finance/recom/{}/'.format(instance.contract.project.id)
	field = 'inv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)