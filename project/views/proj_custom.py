import datetime, io, csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from project.models import Project
from conf.utils import hash_md5
from users.decorators import allowed_users
from sigp.utils import get_roles

#
@allowed_users(allowed_roles=['sigp_admin','sig_uivp','sigp_div','sigp_dna','sigp_dnof','sigp_op','sigp_bd'])
def uvipProjCustomList(request):
	group = get_roles(request)
	objects = Project.objects.all()
	context = {
		'group': group, 'objects': objects,
		'module_name': 'Modulu Projetu', 'title': f'Lista Projetu', 'legend': f'Lista Projetu'
	}
	return render(request, 'project_uvip/custom_list.html', context)
#

@allowed_users(allowed_roles=['sigp_admin'])
def uvipProjHashUpdate(request):
	objs = Project.objects.all()
	for obj in objs:
		obj.hashed = hash_md5(str(obj.id))
		obj.save()
	messages.success(request, f'Atualiza ona.')
	return redirect('uvip-proj-custom-list')
#
@allowed_users(allowed_roles=['sigp_admin'])
@login_required
def uvipProjImport(request):
	group = get_roles(request)
	if request.method == 'POST':
		csv_file = request.FILES['fupload']
		if not csv_file.name.endswith('.csv'):
			messages.error(request, f'File tenke iha formatu CSV.')
		data_set = csv_file.read().decode('latin-1')
		io_string = io.StringIO(data_set)
		next(io_string)
		for column in csv.reader(io_string, delimiter=',', quotechar="|"):
			check = Project.objects.filter(id=column[0]).first()
			if not check:
				desc,is_cont = None,False
				if column[3]: desc = column[3]
				if column[4]: is_cont = column[4]
				_, created = Project.objects.update_or_create(
					id = column[0],
					code = column[1],
					name = column[2],
					desc = desc,
					is_cont = is_cont,
					book_id = column[5],
					capital_id = column[6],
					capital2_id = column[7],
					fund_id = column[8],
					owner_id = column[9],
					pcategory_id = column[10],
					ptype_id = column[11],
					sector_id = column[12],
					status_id = column[13],
					statusproj_id = column[14],
					year_id = column[15],
					pcat_id = column[16],
					is_adn = column[17],
					is_end = column[18],
					name2 = column[19],
					is_active = True,
					is_lock = False,
					user = request.user,
					datetime=datetime.datetime.now(),
					hashed = hash_md5(str(column[0]))
				)
				messages.success(request, f'Importa sucesu.')
			else:
				messages.warning(request, f'ID iha ona.')
		return redirect('uvip-proj-list')
	context = {
		'group':group,
		'title': 'Importa Projetu', 'legend': 'Projetu'
	}
	return render(request, 'project_uvip/import.html', context)