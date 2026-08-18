import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_cont(instance, filename):
	upload_to = 'contract/{}/'.format(instance.contract.project.code)
	number = instance.contract.number.replace("/","-")
	field = 'cont'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_inv(instance, filename):
	upload_to = 'finance/{}/'.format(instance.contract.project.id)
	number = instance.contract.number.replace("/","-")
	field = 'inv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,number,instance.number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cert_pay(instance, filename):
	upload_to = 'finance/{}/'.format(instance.contract.project.id)
	number = instance.contract.number.replace("/","-")
	field = 'certpay'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,number,instance.number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_inv_sp(instance, filename):
	upload_to = 'finance/inv/{}/'.format(instance.invoice.id)
	number = instance.invoice.number.replace("/","-")
	field = 'letteracom'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,number,instance.number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)