import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_inv_disp(instance, filename):
	upload_to = 'inv/{}/'.format(instance.cont.project.id)
	field = 'disp'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_inv(instance, filename):
	upload_to = 'inv/{}/'.format(instance.cont.project.id)
	field = 'inv'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_inv_let(instance, filename):
	upload_to = 'inv/{}/'.format(instance.inv.cont.project.id)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)


def upload_inv_let_dev_adn(instance, filename):
	upload_to = 'inv/{}/'.format(instance.invlet.id)
	field = 'let_dev_adn'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)


def upload_adn(instance, filename):
	upload_to = 'inv/{}/'.format(instance.inv.cont.project.id)
	field = 'inv_adn'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_cert(instance, filename):
	upload_to = 'inv/{}/'.format(instance.inv.cont.project.id)
	field = 'cert'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_recom(instance, filename):
	upload_to = 'inv/{}/'.format(instance.inv.cont.project.id)
	field = 'recom'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
