from .models import Project
import django_filters

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['project_type', 'is_approved']