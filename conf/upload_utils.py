import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_sp(instance, filename):
	upload_to = 'letters/{}/'.format(instance.letter.project.code)
	number = instance.letter.number.replace("/", "-")
	field = 'sp'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.letter.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_adn(instance, filename):
	upload_to = 'letters/{}/'.format(instance.letter.project.code)
	number = instance.letter.number.replace("/", "-")
	field = 'adn'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}_{}.{}'.format(field,instance.letter.date,number,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_plan(instance, filename):
	upload_to = 'upload_planletters/{}/files/'.format(instance.letter.project.code)
	field = 'plan'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.letter.date,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)
