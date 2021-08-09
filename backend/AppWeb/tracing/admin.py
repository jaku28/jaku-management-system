from django.contrib import admin
from . import models

class EvaluationAdmin(admin.ModelAdmin):
	list_display = ('name', 'call', 'date', 'max_points')

class CriteriaAdmin(admin.ModelAdmin):
	list_display = ('name', 'evaluation', 'description', 'weight')

class MentoringAdmin(admin.ModelAdmin):
	list_display = ('mentor', 'project', 'date', 'time')

admin.site.register(models.Evaluation, EvaluationAdmin)
admin.site.register(models.Criteria, CriteriaAdmin)
admin.site.register(models.Mentoring, MentoringAdmin)
admin.site.register(models.EvaluationJury)
admin.site.register(models.CriteriaProject)
admin.site.register(models.EvaluationProject)
admin.site.register(models.Activity)
admin.site.register(models.EvaluationSummary)
admin.site.register(models.Interview)