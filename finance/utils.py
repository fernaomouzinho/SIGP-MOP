import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_cpvreq(instance, filename):
	upload_to = 'finance/{}/'.format(instance.proj.id)
	field = 'cpvreq'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cpv(instance, filename):
	upload_to = 'finance/{}/'.format(instance.proj.code)
	field = 'cpv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_po(instance, filename):
	upload_to = 'finance/{}/'.format(instance.cont.project.id)
	number = instance.number.replace("/", "-")
	field = 'po'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_sp(instance, filename):
	upload_to = 'finance/{}/'.format(instance.cpvreq.project.id)
	number = instance.number.replace("/","-")
	field = 'cpvreq_sp'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cpv_let(instance, filename):
	upload_to = 'finance/{}/'.format(instance.cpv.proj.id)
	number = instance.number.replace("/","-")
	field = 'cpv_let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_po_let(instance, filename):
	upload_to = 'finance/{}/'.format(instance.po.cont.project.id)
	number = instance.number.replace("/","-")
	field = 'po_let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_prt(instance, filename):
	upload_to = 'finance/{}/'.format(instance.cont.project.id)
	field = 'prt'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.inv.id,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_ev(instance, filename):
	upload_to = 'finance/{}/'.format(instance.cont.project.id)
	field = 'ev'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.inv.cont.project.id,instance.inv.id,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_fin_files(instance, filename):
	upload_to = 'finance/{}/files/{}/'.format(instance.proj.id,instance.inv.id)
	field = 'file'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.proj.id,instance.inv.id,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
