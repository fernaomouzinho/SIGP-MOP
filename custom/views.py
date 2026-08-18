from django.shortcuts import render
from .models import AdministrativePost, Aldeia, Village

def load_posts(request):
	mun_id = request.GET.get('municipality')
	posts = AdministrativePost.objects.filter(municipality_id=mun_id).order_by('name')
	return render(request, 'custom/posts_dropdown.html', {'posts': posts})

def load_villages(request):
	post_id = request.GET.get('post')
	villages = Village.objects.filter(administrativepost_id=post_id).order_by('name')
	return render(request, 'custom/villages_dropdown.html', {'villages': villages})

def load_aldeias(request):
	vil_id = request.GET.get('vil')
	aldeias = Aldeia.objects.filter(village_id=vil_id).order_by('name')
	return render(request, 'custom/aldeias_dropdown.html', {'aldeias': aldeias})
