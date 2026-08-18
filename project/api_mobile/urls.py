from django.urls import path
from project.api_mobile.view import ProjectListView

urlpatterns = [
    path('proj/list/', ProjectListView.as_view(), name='project-list'),
]