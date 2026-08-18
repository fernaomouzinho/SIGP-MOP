from rest_framework import generics
from project.models import Project
from project.api_mobile.serializers import ProjectSerializer

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer