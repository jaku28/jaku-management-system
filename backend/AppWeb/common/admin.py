from django.contrib import admin
from .models import BudgetRegistry, Call, Entity, Project, New, Event, DefaultTask, Task, EventRegister, DefaultWorkshop, Workshop, UserProject, BigForm, FormConfig, BudgetRegistry
admin.site.site_header = 'Jaku'
admin.site.site_title = 'Jaku'
admin.site.index_title = 'Jaku'

class CallAdmin(admin.ModelAdmin):
	list_display = ('name', 'entity', 'due_date', 'preparation_start', 'final_date')

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'leader', 'call')

class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'date')

class TaskAdmin(admin.ModelAdmin):
	list_display = ('name', 'event', 'assign_to', 'assigned_date', 'due_date')

class WorkshopAdmin(admin.ModelAdmin):
	list_display = ('name', 'call', 'description', 'temary')

admin.site.register(Call, CallAdmin)
admin.site.register(Entity)
admin.site.register(Project, ProjectAdmin)
admin.site.register(New)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegister)
admin.site.register(DefaultTask)
admin.site.register(Task, TaskAdmin)
admin.site.register(DefaultWorkshop)
admin.site.register(UserProject)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(BigForm)
admin.site.register(FormConfig)
admin.site.register(BudgetRegistry)
