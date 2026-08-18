import os, datetime
from pytz import timezone
from uuid import uuid4

now = datetime.datetime.now(timezone("Asia/Dili"))

def upload_eval(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_disp(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'disp'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_tor(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'tor'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_boq(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'boq'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_design(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'design'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_spec(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'specification'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_mapq(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'map_quarry'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_docoth(instance, filename):
	upload_to = 'eval/{}/'.format(instance.eval.proj.id)
	field = 'doc_other'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

## ADN FILE
def upload_eval_adn(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_eval_adn_boq(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_eval_adn_design(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_eval_adn_spec(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_eval_adn_mapq(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def upload_eval_adn_docoth(instance, filename):
	upload_to = 'eval/adn/{}/'.format(instance.evallet)
	field = 'let'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}.{}'.format(field,instance.pk, ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)