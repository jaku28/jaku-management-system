from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
from .filters import ProjectFilter
from . import models
from accounts.models import User, Profile, ProfileJury, ProfileMentor, ProfileCoach
from tracing.models import EvaluationProject
from .models import New
from .forms import NewForm, ProjectForm, EventForm, AccountForm, UserForm, CallForm
import datetime
import xlwt
from .email_utils import email_util

#here it checks if the user is entrepreneur or admin type
def system_home(request):
	if request.user.groups.filter(name='Emprendedor').exists(): 
		return redirect(reverse('common:entrepreneurhome'))
	if request.user.groups.filter(Q(name='Administrador') | Q(name='Personal')).exists(): 
		return redirect(reverse('common:adminhome'))
	elif request.user.groups.filter(name='Mentor').exists(): 
		return redirect(reverse('tracing:mentorhome'))
	elif request.user.groups.filter(name='Jurado').exists():
		return redirect(reverse('tracing:juryhome'))
	if request.user.groups.filter(name='Coach').exists():
		return redirect(reverse('tracing:coachhome'))
	else:
		return redirect(reverse('accounts:login'))

# form for register a new request for create an entrepreneur user
def entrepreneur_registry(request):
	title = 'Registrar sus datos'
	if request.method == 'POST':
		form_profile = AccountForm(request.POST)
		form_user = UserForm(request.POST)
		group = Group.objects.get(name='Emprendedor')
		pwd = User.objects.make_random_password()
		print(pwd)

		if (form_profile.is_valid() and form_user.is_valid() ):
			user = form_user.save()
			user.email = user.username
			user.set_password(pwd)
			user.is_active = False
			user.profile = form_profile.save(commit=False)
			user.profile.is_pending = True
			user.profile.temp_pwd = pwd
			user.save()
			user.groups.add(group)
			return render(request, 'entrepreneur_registry/registry_done.html')
	else:
		form_profile = AccountForm()
		form_user = UserForm()
	return render(request, 'entrepreneur_registry/form.html', locals())

#show request list
@login_required
@permission_required('common.is_jaku_staff')
def request_list(request):
	title = 'Lista de solicitudes'
	query_set = Profile.objects.select_related('user').filter(user__groups__name='Emprendedor').filter(is_pending=True)
	r_list = reversed(list(query_set))
	return render(request, 'entrepreneur_registry/request_entrepreneur/request_list.html', locals())


#show request detail
@login_required
@permission_required('common.is_jaku_staff')
def request_detail(request, r_id):
	title = 'Detalle de solicitud'
	requesting_user = Profile.objects.select_related('user').get(pk=r_id)

	return render(request, 'entrepreneur_registry/request_entrepreneur/detail.html', locals())

#for change is_pending 
@login_required
@permission_required('auth.add_user')
def accept_entrepreneur(request, r_id):
	profile = Profile.objects.select_related('user').get(pk=r_id)
	profile.is_pending = False
	profile.user.is_active = True
	profile.user.save()
	profile.save()
	email_util().send_email_html(request, profile, True)

	return redirect(reverse('common:requestlist'))

#for reject a request of entrepreneur
@login_required
@permission_required('auth.delete_user')
def reject_entrepreneur(request, r_id):
	user = User.objects.get(profile=r_id)
	profile = get_object_or_404(Profile, pk=r_id)
	email_util().send_email_html(request, profile, False)
	user.delete()
	profile.delete()
	
	return redirect(reverse('common:requestlist'))

# VIEWS FOR ADMIN AND PERSONAL VIEW
#can create a new user
@login_required
@permission_required('auth.add_user')
def create_user(request):
	title = 'Agregar administrador'

	if request.method == 'GET':
		return render(request, 'common/users/form.html', locals())

	username = request.POST.get('username')
	if models.User.objects.filter(username=username):
		error = "Ya existe el usuario: " + username + "."			
		return render(request, 'common/users/form.html', locals())
	
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	email = request.POST.get('email')
	group = Group.objects.get(name='Administrador') 
	pwd = request.POST.get('pwd')

	user = models.User(username=username, first_name=first_name, last_name=last_name, email=email)
	user.set_password(pwd)
	user.save()
	user.groups.add(group)
	
	return redirect(reverse('common:userlist'))

#shows all users as a list
@login_required
@permission_required('common.is_jaku_staff')
def user_list(request):
	title = 'Lista de administradores'
	query_set = models.User.objects.filter(groups__name='Administrador')
	users = reversed(list(query_set))
	return render(request, 'common/users/list.html', locals())

#shows user detail
@login_required
@permission_required('common.is_jaku_staff')
def user_detail(request, user_id):
	title = 'Detalle de usuario'
	user = models.User.objects.prefetch_related('groups').get(pk=user_id)

	return render(request, 'common/users/detail.html', locals())

#can edit a user
@login_required
@permission_required('auth.change_user')
def edit_user(request, user_id):
	title = 'Editar administrador'
	user = models.User.objects.prefetch_related('groups').get(pk=user_id)

	if request.method == 'GET': 
		groups = Group.objects.all()
		return render(request, 'common/users/edit.html', locals())

	user_first_name = request.POST.get('first_name')
	user_last_name = request.POST.get('last_name')
	user_email = request.POST.get('email')
	
	if request.POST.get('password'):
		pwd = request.POST.get('password')
		user.set_password(pwd)

	user.first_name = user_first_name
	user.last_name = user_last_name
	user.email = user_email
	user.save()

	return redirect(reverse('common:userlist'))

#can delete a user
@login_required
@permission_required('auth.delete_user')
def delete_user(request, user_id):
	user = get_object_or_404(models.User, pk=user_id)
	user.delete()
	
	return redirect(reverse('common:userlist'))


#can create an event
@login_required
@permission_required('common.add_event')
def create_event(request):
	title = 'Agregar evento'
	if request.method == 'GET':	
		form = EventForm()
		context = {
			"form": form,
			"title": title
		}
	else:
		form = EventForm(request.POST, request.FILES)
		context = {
			"form": form
		}
		if form.is_valid():		
			event = form.save()
			return redirect(reverse('common:defaulttasklist', kwargs={'event_id':event.id}))
	return render(request, 'common/event/form.html', context)

#edit event's information
@login_required
@permission_required('common.change_event')
def edit_event(request, event_id):
	title = 'Editar evento'
	
	event = models.Event.objects.get(id = event_id)
	if request.method == 'GET':
		form = EventForm(instance = event)
		context = {
			"form":form,
			"title": title
		}
	else:
		form = EventForm(request.POST, request.FILES, instance = event)
		context = {
			"form": form
		}
		if form.is_valid():
			form.save()
			return redirect('common:eventlist')
	return render(request, 'common/event/edit.html', locals())

#edit (add) tasks assigned on an event
@login_required
@permission_required('common.change_event')
def edit_event_tasks(request, event_id):
	title = 'Tareas asignadas al evento'
	event = models.Event.objects.get(pk=event_id)
	personal_users = models.User.objects.filter(groups__name='Personal')
	event_tasks = models.Task.objects.select_related('assign_to').filter(event__id=event_id)

	if request.method == 'GET':
		return render(request, 'common/event/edit_tasks.html', locals())
	
	new_task_name = request.POST.getlist('task_name')
	assign_to_ids = request.POST.getlist('personal_users')
	assigned_dates = request.POST.getlist('assigned_date')
	due_dates = request.POST.getlist('due_date')
	assigned_users = []


	for a in assign_to_ids:
		if a == 'Ninguno':
			assigned_users.append(a)
		else:	
			assigned_users.append(models.User.objects.get(id=a))
	
	c = 0

	for t,f,af in zip(new_task_name, due_dates, assigned_dates):
		if t == '' and assigned_users[c] == 'Ninguno' and f == '':
			return redirect(reverse('common:eventlist'))
		else:
			if assigned_users[c] == 'Ninguno':
				if f == '':
					task = models.Task(name=str(t), event=event)
				else:
					task = models.Task(name=str(t), event=event, due_date=f, assigned_date=af)
			else:
				if f == '':
					task = models.Task(name=str(t), event=event, assign_to=assigned_users[c])
				else:
					task = models.Task(name=str(t), event=event, assign_to=assigned_users[c], due_date=f, assigned_date=af)
			
			c = c+1
			task.save()

	c = 0
	
	return redirect(reverse('common:eventlist'))

#delete a  task assigned on an event
@login_required
@permission_required('common.change_event')
def delete_event_task(request, event_id, task_id):
	task = get_object_or_404(models.Task, pk=task_id)
	task.delete()

	return redirect(reverse('common:editeventtasks', kwargs={'event_id':event_id}))

#deletes an event
@login_required
@permission_required('common.delete_event')
def delete_event(request, event_id):
	event = get_object_or_404(models.Event, pk=event_id)
	event.delete()
	
	return redirect('common:eventlist')

#show event's information
@login_required
@permission_required('common.is_jaku_staff')
def event_detail(request, event_id):
	title = 'Detalle de evento'
	event = get_object_or_404(models.Event, pk=event_id)
	
	return render(request, 'common/event/detail.html', locals())

#show event list
@login_required
@permission_required('common.is_jaku_staff')
def show_events(request):
	title = 'Lista de eventos'
	query_set = models.Event.objects.all()
	events = reversed(list(query_set))
	return render(request, 'common/event/list.html', locals())

#show preloaded tasks for that event
@login_required
@permission_required('common.add_event')
def show_default_tasks(request, event_id):
	title = 'Tareas pre-cargadas'
	event = models.Event.objects.get(id=event_id)
	personal_users = models.User.objects.filter(groups__name='Personal')

	if request.method == 'GET':	
		default_tasks = models.DefaultTask.objects.all()
		return render(request, 'common/task/list_default_task.html', locals())

	default_task_name = request.POST.getlist('nametask')
	assign_to_ids = request.POST.getlist('personalusers')
	due_dates = request.POST.getlist('due_date')
	assigned_dates = request.POST.getlist('assigned_date')
	assigned_users = []
	
	for a in assign_to_ids:
		if a == 'Ninguno':
			assigned_users.append(a)
		else:
			assigned_users.append(models.User.objects.get(id=a))
	count = 0
	for d,f,af in zip(default_task_name, due_dates, assigned_dates):
		if assigned_users[count] == 'Ninguno':
			if f == '':
				task = models.Task(name=str(d), event=event)
			else: 
				task = models.Task(name=str(d), event=event, assigned_date=af, due_date=f)
		else:
			if f == '':
				task = models.Task(name=str(d), event=event, assign_to=assigned_users[count])
			else:
				task = models.Task(name=str(d), event=event, assign_to=assigned_users[count], assigned_date=af, due_date=f)
		
		count = count+1
		task.save()
	count = 0
	if request.POST.get("save_tasks"):
		return redirect(reverse('common:eventlist'))
	else:
		return redirect(reverse('common:updateevent', kwargs={'event_id':event.id}))

#allows adding new task (this task won't be saved in preloaded task) on an event
@login_required
@permission_required('common.add_event')
def update_event(request, event_id):
	title = 'Agregar tareas adicionales'
	event = models.Event.objects.get(id=event_id)
	personal_users = models.User.objects.filter(groups__name='Personal')

	if request.method == 'GET':
		return render(request, 'common/event/update_event.html', locals())

	new_task_name = request.POST.getlist('newTask')
	n_assign_to_ids = request.POST.getlist('n_personalusers')
	n_assigned_dates = request.POST.getlist('n_assigned_date')
	n_due_dates = request.POST.getlist('n_due_date')
	n_assigned_users = []


	for na in n_assign_to_ids:
		if na == 'Ninguno':
			n_assigned_users.append(na)
		else:	
			n_assigned_users.append(models.User.objects.get(id=na))
	
	n_count = 0

	for n,nf,af in zip(new_task_name, n_due_dates, n_assigned_dates):
		if n == '' and n_assigned_users[n_count] == 'Ninguno' and nf == '':
			return redirect(reverse('common:eventlist'))
		else:
			if n_assigned_users[n_count] == 'Ninguno':
				if nf == '':
					task = models.Task(name=str(n), event=event)
				else:
					task = models.Task(name=str(n), event=event, due_date=nf, assigned_date=af)
			else:
				if nf == '':
					task = models.Task(name=str(n), event=event, assign_to=n_assigned_users[n_count])
				else:
					task = models.Task(name=str(n), event=event, assign_to=n_assigned_users[n_count], due_date=nf, assigned_date=af)
			
			n_count = n_count+1
			task.save()

	n_count = 0
	
	return redirect(reverse('common:eventlist'))

#shows all entrepreneur users that are registered in an event
@login_required
@permission_required('common.is_jaku_staff')
def attendee_list(request, event_id):
	title = 'Asistentes al evento'
	event = models.Event.objects.get(pk=event_id)
	query_set = models.EventRegister.objects.select_related('user').filter(event=event)
	registry_of_event = reversed(list(query_set))

	return render(request, 'common/event/attendee_list.html', locals())



#shows a list of existing preloaded tasks 
@login_required
@permission_required('common.is_jaku_staff')
def list_of_default_tasks(request):
	title = 'Tareas pre-cargadas'

	query_set = models.DefaultTask.objects.all()
	defaulttasks = reversed(list(query_set))
	return render(request, 'common/default_task/list.html', locals())


#can create a new preloaded task
@login_required
@permission_required('common.add_defaulttask')
def create_default_task(request):
	title = 'Agregar tarea pre-cargada'

	if request.method == 'GET':
		return render(request, 'common/default_task/form.html', locals())
	
	defaulttask_name = request.POST.get('name')
	defaulttask = models.DefaultTask(name=defaulttask_name)
	defaulttask.save()
	return redirect('common:listofdefaulttasks')

#can edit a preloaded task
@login_required
@permission_required('common.change_defaulttask')
def edit_default_task(request, default_task_id):
	title = 'Editar tarea pre-cargada'
	defaulttask = get_object_or_404(models.DefaultTask, pk=default_task_id)

	if request.method == 'GET':
		return render(request, 'common/default_task/edit.html', locals())

	defaulttask_name = request.POST.get('name')
	defaulttask.name = defaulttask_name
	defaulttask.save()

	return redirect('common:listofdefaulttasks')

#can delete a preloaded task
@login_required
@permission_required('common.delete_defaulttask')
def delete_default_task(request, default_task_id):
	defaulttask = get_object_or_404(models.DefaultTask, pk=default_task_id)
	defaulttask.delete()
	
	return redirect('common:listofdefaulttasks')

#shows the user in session assign tasks
@login_required
@permission_required('common.mark_as_done_task')
def show_my_assigned_tasks(request):
	title = 'Mis tareas asignadas'
	query_set = models.Task.objects.select_related('event').filter(assign_to=request.user)
	assigned_tasks = reversed(list(query_set))
	 
	if request.method == 'GET':
		return render(request, 'common/assigned_task/list.html', locals())


#for mark a task as done (only if the user is 'Personal')
@login_required
@permission_required('common.mark_as_done_task')
def mark_as_done(request, task_id):
	task = models.Task.objects.get(pk=task_id)
	task.is_done = True
	task.save()

	return redirect('common:showmyassignedtasks')

#for mark a task as not done (only if the user is 'Personal')
@login_required
@permission_required('common.mark_as_done_task')
def mark_as_not_done(request, task_id):
	task = models.Task.objects.get(pk=task_id)
	task.is_done = False
	task.save()

	return redirect('common:showmyassignedtasks')

def assign_task():
	if request.method == 'GET':
		return render(request, 'common/event/') 

# this function allows the admin to see the news from the most current to the oldest
@login_required
@permission_required('common.is_jaku_staff')
def show_news(request):
	query_set = New.objects.all()
	news = reversed(list(query_set))
	context = {
		'news': news
	}
	return render(request, 'common/new/list.html', context)

""" allows to admin to create a new with a form defined in forms.py
the first time the admin enter is get and redirects to form
the second time is post and it will bring the form data
if all information inserted in the form it is valid it saves it
and finally redirect to the news list """
@login_required
@permission_required('common.add_new')
def create_news(request):
	if request.method == 'GET':	
		form = NewForm()
		context = {
			"form": form
		}
	else:
		form = NewForm(request.POST, request.FILES)
		context = {
			"form": form
		}
		if form.is_valid():		
			form.save()
			return redirect('common:new')
	return render(request, 'common/new/new_form.html', context)

# this function is similar to create only that edits the data using the news id and redirect to the news list
@login_required
@permission_required('common.change_new')
def edit_news(request, new_id):
	new = New.objects.get(id = new_id)
	form = None
	if request.method == 'GET':
		form = NewForm(instance = new)	
	else:
		form = NewForm(request.POST, request.FILES, instance = new)		
		if form.is_valid():
			form.save()
			return redirect('common:new')
	return render(request, 'common/new/edit_form.html', locals())

# the new is deleted by means of the id with a previus confirmation notification and redirect to the news list
@login_required
@permission_required('common.delete_new')
def delete_news(request, new_id):
	new = New.objects.get(id = new_id)
	new.delete()
	return redirect('common:new')

#Create a new call
@login_required
@permission_required('common.add_call')
def create_call(request):
	title = 'Agregar Convocatoria'
	entities = models.Entity.objects.all()
	if request.method == 'GET':	
		form = CallForm()
		context = {
			"form": form,
			"entities": entities
		}
	else:
		form = CallForm(request.POST, request.FILES)
		context = {
			"form": form
		}
		if form.is_valid():
			call = form.save()
			return redirect(reverse('common:defaultworkshoplist', kwargs={'call_id':call.id}))
	return render(request, 'common/call/form.html', locals())
	
#show preloaded tasks for that call
@login_required
@permission_required('common.add_call')
def show_default_workshops(request, call_id):
	title = 'Talleres predeterminados'
	call = models.Call.objects.get(id=call_id)

	if request.method == 'GET':	
		default_workshops = models.DefaultWorkshop.objects.all()
		return render(request, 'common/workshop/list_default_workshop.html', locals())

	default_workshop_name = request.POST.getlist('nameworkshop')
	for w in default_workshop_name:
		dw = models.DefaultWorkshop.objects.get(id=w)
		workshop = models.Workshop(name=dw.name, call=call, description=dw.description, temary=dw.temary)
		workshop.save()
	
	count = 0
	if request.POST.get("save_workshops"):
		return redirect(reverse('common:calllist'))
	else:
		return redirect(reverse('common:editcall', kwargs={'call_id':call.id}))

#allows adding new workshop (this workshop won't be saved in preloaded workshops) on an call
@login_required
@permission_required('common.add_call')
def edit_call(request, call_id):
	title = 'Agregar talleres adicionales'
	call = models.Call.objects.get(id=call_id)

	if request.method == 'GET':
		return render(request, 'common/call/edit_call.html', locals())

	new_workshop_name = request.POST.getlist('workshop_name')
	new_workshop_description = request.POST.getlist('workshop_description')
	new_workshop_temary = request.POST.getlist('workshop_temary')

	for name, description, temary in zip(new_workshop_name, new_workshop_description, new_workshop_temary):
		if name == '' and description == '' and temary == '':
			return redirect(reverse('common:calllist'))
		workshop = models.Workshop(name=str(name), call=call, description=str(description), temary=str(temary))
		workshop.save()

	n_count = 0
	
	return redirect(reverse('common:calllist'))

#edit (add) workshops assigned on an call
@login_required
@permission_required('common.change_call')
def edit_call_workshops(request, call_id):
	title = 'Talleres asignados a la convocatoria'
	call = models.Call.objects.get(pk=call_id)
	call_workshops = models.Workshop.objects.filter(call__id=call_id)

	if request.method == 'GET':
		return render(request, 'common/call/edit_workshops.html', locals())
	
	new_workshop_name = request.POST.getlist('workshop_name')
	new_workshop_description = request.POST.getlist('workshop_description')
	new_workshop_temary = request.POST.getlist('workshop_temary')
	
	for name, description, temary in zip(new_workshop_name, new_workshop_description, new_workshop_temary):
		if name == '' and description == '' and temary == '':
			return redirect(reverse('common:calllist'))
		workshop = models.Workshop(name=str(name), call=call, description=str(description), temary=str(temary))
		workshop.save()

	c = 0
	
	return redirect(reverse('common:calllist'))

#delete a  workshop assigned on an call
@login_required
@permission_required('common.change_call')
def delete_call_workshop(request, call_id, workshop_id):
	workshop = get_object_or_404(models.Workshop, pk=workshop_id)
	workshop.delete()

	return redirect(reverse('common:editcallworkshops', kwargs={'call_id':call_id}))

#Show call list
@login_required
@permission_required('common.is_jaku_staff')
def show_calls(request):
	title = 'Lista de convocatorias'
	query_set = models.Call.objects.select_related('entity').all()
	calls = reversed(list(query_set))
	today = datetime.date.today()
	context = {
		"title": title,
		"calls": calls,
		"today": today
	}
	return render(request, 'common/call/list.html', context)

#Show an entire call
@login_required
@permission_required('common.is_jaku_staff')
def call_detail(request, call_id):
	call = get_object_or_404(models.Call, pk=call_id)
	entities = models.Entity.objects.all()
	call_workshops = models.Workshop.objects.filter(call__id=call_id)
	today = datetime.date.today()
	context = {
		"call": call,
		"entities": entities,
		"today": today,
		"call_workshops": call_workshops
	}
	
	return render(request, 'common/call/call_detail.html', context)

#Update a call (only when the due date didn't expire)
@login_required
@permission_required('common.change_call')
def update_call(request, call_id):
	title = 'Editar Convocatoria'
	call = get_object_or_404(models.Call, pk=call_id)
	entities = models.Entity.objects.all()

	if call.has_projects == 0:
		if request.method == 'POST':
			form = CallForm(request.POST, request.FILES, instance = call)
			context = {
				"form": form
			}
			if form.is_valid():
				form.save()

		else:
			form = CallForm(instance = call)
			context = {
				"form":form,
				"entities":entities
			}
			return render(request, 'common/call/update_call.html', locals())

	return redirect('common:calllist')	
	
#Delete a call (only when the due date didn't expire)
@login_required
@permission_required('common.delete_call')
def delete_call(request, call_id):
	call = get_object_or_404(models.Call, pk=call_id)
	
	if call.has_projects == 0:
		call.delete()
	

	return redirect('common:calllist')

#shows a list of existing entities 
@login_required
@permission_required('common.is_jaku_staff')
def list_of_entities(request):
	title = 'Entidades'

	query_set = models.Entity.objects.all()
	entities = reversed(list(query_set))
	return render(request, 'common/entity/list.html', locals())


#can create a new entity
@login_required
@permission_required('common.add_entity')
def create_entity(request):
	title = 'Agregar entidad'

	if request.method == 'GET':
		return render(request, 'common/entity/form.html', locals())
	
	entity_name = request.POST.get('name')

	if models.Entity.objects.filter(name=entity_name):
		error = "Ya existe una entidad creada con el nombre " + entity_name + "."
		return render(request, 'common/entity/form.html', locals())

	entity = models.Entity(name=entity_name)
	entity.save()
	return redirect('common:listofentities')

#can edit a entity
@login_required
@permission_required('common.change_entity')
def edit_entity(request, entity_id):
	title = 'Editar entidad'
	entity = get_object_or_404(models.Entity, pk=entity_id)

	if request.method == 'GET':
		return render(request, 'common/entity/edit.html', locals())

	entity_name = request.POST.get('name')

	if models.Entity.objects.filter(name=entity_name):
		error = "Ya existe una entidad creada con el nombre " + entity_name + "."
		return render(request, 'common/entity/edit.html', locals())
	
	entity.name = entity_name
	entity.save()

	return redirect('common:listofentities')

#shows all projects that are registered in an call
@login_required
@permission_required('common.is_jaku_staff')
def call_projects_list(request, call_id):
	title = 'Proyectos'
	call = models.Call.objects.get(pk=call_id)
	registry_of_project= models.Project.objects.select_related('call').filter(call=call)
	project_filter = ProjectFilter(request.GET, queryset=registry_of_project)
	today = datetime.date.today()
	
	return render(request, 'common/call/projects_list.html', locals())

#Completes the reviews of the projects of a call
@login_required
def finish_review(request, call_id):
	call = get_object_or_404(models.Call, pk=call_id)
	call.is_reviewed = True
	call.save()

	projects = models.Project.objects.select_related('call').filter(call=call)
	for p in projects:
		projects_group = models.UserProject.objects.select_related('project').filter(project=p)
		for pr in projects_group:
			email_util().send_email_filter(request, pr.user, pr.project.is_approved)

	return redirect('common:callprojectslist', call.id)

#shows project detail
@login_required
@permission_required('common.is_jaku_staff')
def call_project_detail(request, project_id):
	title = 'Detalle de proyecto'
	project = models.Project.objects.select_related('call').get(pk=project_id)
	leader = Profile.objects.get(pk=project.leader)
	today = datetime.date.today()

	return render(request, 'common/call/project_detail.html', locals())

#approve a project after the call's due date and before call has an evaluation
@login_required
@permission_required('common.is_jaku_staff')
def approve_project(request, project_id):
	project = models.Project.objects.get(id=project_id)
	call = project.call
	today = datetime.date.today()
	if call.due_date < today:
		project.is_approved = '2'
		project.save()
	return redirect('common:callprojectslist', call.id)

#reject a project after the call's due date and before call has an evaluation
@login_required
@permission_required('common.is_jaku_staff')
def reject_project(request, project_id):
	project = models.Project.objects.get(id=project_id)
	call = project.call
	today = datetime.date.today()
	if call.due_date < today:
		project.is_approved = '3'
		project.save()
	return redirect('common:callprojectslist', call.id)

def export(request, event_id):
	e = models.Event.objects.get(pk=event_id)

	response = HttpResponse(content_type='application/ms-excel')
	filename = 'asistentes_' + str(event_id) + '.xls' 
	rp = 'attachment; filename=' + str(filename)
	response['Content-Disposition'] = rp

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Asistentes') # this will make a sheet named Users Data

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	title_sheet = 'Lista de Asistentes al evento: ' + e.title 
	
	ws.write(row_num, 0, title_sheet, font_style)

	row_num += 1
	columns = ['#', 'Apellidos', 'Nombres', 'Correo', 'DNI', 'Teléfono', 'Especialidad',]

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = models.EventRegister.objects.filter(event__id=event_id).select_related('user').values_list('user__last_name', 'user__first_name', 'user__email', 'user__profile__dni', 'user__profile__phone_number', 'user__profile__specialty')
	for row in rows:
		row_num += 1
		ws.write(row_num, 0, row_num-1, font_style)
		for col_num in range(len(row)):
			ws.write(row_num, col_num+1, row[col_num], font_style)

	wb.save(response)

	return response



# VIEWS FOR ENTREPRENEUR VIEW
#show all events
@login_required
@permission_required('common.is_entrepreneur')
def e_show_events(request):
	title = 'Eventos'
	today = datetime.date.today()
	events = models.Event.objects.filter(date__gte=today)
	user_events = models.EventRegister.objects.select_related('event').filter(user=request.user)
	events_registered = {}
	for ue in user_events:
		events_registered[ue.event.id] = True
	for e in events:
		try:
			e.is_registered = events_registered[e.id]
		except: 
			pass

	return render(request, 'common/e_event/list.html', locals())

#shows entrepreneur user's events
@login_required
@permission_required('common.is_entrepreneur')
def e_show_my_events(request):
	title = 'Mis eventos'
	query_set = models.EventRegister.objects.select_related('event').filter(user=request.user)
	my_events = reversed(list(query_set))

	return render(request, 'common/e_event/my_events.html', locals()) 

#for registering an entrepreneur user in an event
@login_required
def register(request, event_id):
	event = models.Event.objects.get(pk=event_id)
	registry = models.EventRegister(event=event, user=request.user)
	registry.save()
	return redirect('common:e_showevents')

#for leaving an event (for entrepreneur user)
@login_required
def leave(request, event_id):
	event = models.Event.objects.get(pk=event_id)
	registry = models.EventRegister.objects.get(event=event, user=request.user)
	registry.delete()

	return redirect('common:e_showevents')

#can create a new project
@login_required
@permission_required('common.is_entrepreneur')
def create_project(request, call_id):
	call = models.Call.objects.get(pk = call_id)
	user_projects = models.UserProject.objects.select_related('project').filter(user=request.user)
	users_project = models.UserProject.objects.select_related('project').values('user')
	profiles = Profile.objects.select_related('user').values('user')
	profiles_ = []

	for p in profiles:
		if not(p in users_project):
			profiles_.append(Profile.objects.get(user__id = p['user']))

	is_already_registered_in_convocatory = False
	is_already_registered_in_entity = False
	today = datetime.date.today()

	for up in user_projects:
		if up.project.call == call:
			is_already_registered_in_convocatory = True
		if up.project.call.entity == call.entity and up.project.call.due_date >= today:
			is_already_registered_in_entity = True
	
	if is_already_registered_in_convocatory or is_already_registered_in_entity:		
		return render(request, 'common/project/alert_create_project.html')
	else:
		if request.method == 'GET':
			form = ProjectForm()
			context = {
				"title": 'Registro Nuevo Proyecto',
				"form": form,
				"call": call,
				"user": request.user,
				"profiles": profiles_
			}
		else:
			form = ProjectForm(request.POST)
			context = {
				"form": form
			}
			if form.is_valid():
				formc = form.save(commit=False)
				formc.call = models.Call.objects.get(pk = call_id)		
				formc.is_active = True
				leader_profile = Profile.objects.get(user = request.user.id)
				formc.leader = leader_profile.id
				formc.code = create_code(call)
				call.num_projects += 1
				call.has_projects += 1
				call.save()
				formc.save()
				array = request.POST.get('members_id').split()
				for x in array:
					user_ = Profile.objects.get(pk = x)
					registry = models.UserProject(project=formc, user=user_.user)
					registry.save()
					email_util().send_email_entrepreneur(request, user_, formc.name)
				return redirect('common:myprojectslist')
		return render(request, 'common/project/form.html', context)

# function for generate a project code
def create_code(current_call):
	name = current_call.name.split()
	count_letter = 0
	letters = ""
	for word in name:
		if (len(word) > 3 and count_letter < 2):
			letters += word[0]
			count_letter += 1
	letters.upper()
	year = current_call.due_date.strftime('%Y')
	number = str(current_call.num_projects).zfill(3)
	return letters + "-" + year + "-" + number

#can edit a new project
@login_required
@permission_required('common.is_entrepreneur')
def edit_project(request, project_id):	
	project_user = models.UserProject.objects.get(project__id = project_id, user = request.user)
	project = get_object_or_404(models.Project, pk = project_id)
	title = 'Editar Proyecto'
	form = None
	call = project.call
	leader = Profile.objects.get(pk=project.leader)
	user_first_name = request.user.first_name
	user_last_name = request.user.last_name
	profiles = Profile.objects.all()
	if request.method == 'GET':
		form = ProjectForm(instance = project)
	else:
		form = ProjectForm(request.POST, instance = project)		
		if form.is_valid():
			formc = form.save(commit=False)
			nuevo_lider = request.POST.get('new_leader')
			formc.leader = nuevo_lider
			formc.call = call		
			formc.save()
			array = request.POST.get('members_id').split()
			print (array)
			for x in array:
				user_ = Profile.objects.get(pk = x)
				registry = models.UserProject(project=formc, user=user_.user)
				registry.save()
				email_util().send_email_entrepreneur(request, user_, formc.name)
			arrayDel = request.POST.get('members_id_delete').split()
			print (arrayDel)
			for x in arrayDel:
				user_ = Profile.objects.get(pk = x)
				user_project = models.UserProject.objects.get(user = user_.user)
				user_project.delete()
			return redirect('common:myprojectslist')

	if request.user == project_user.user: 
		return render(request, 'common/project/project_edit.html', locals())

	else:
		return HttpResponse('No tiene permisos para visualizar este proyecto')

#Show all the information for a project
@login_required
@permission_required('common.is_entrepreneur')
def my_project_detail(request, project_id):
	project = models.UserProject.objects.get(project__id = project_id, user = request.user)
	context = {
		"project": project,
	}

	if request.user == project.user: 	
		return render(request, 'common/project/project_detail.html', context)
	
	else:
		return HttpResponse('No tiene permisos para visualizar este proyecto')

#For delete a project
@login_required
@permission_required('common.is_entrepreneur')
def delete_project(request, project_id):
	project = models.UserProject.objects.get(project__id = project_id, user = request.user)

	if request.user == project.user:
		call = project.project.call
		call.has_projects -= 1
		call.save()
		project.delete()
	else :
		return HttpResponse('No tiene permisos para visualizar este proyecto')

	return redirect('common:myprojectslist')

#See all the projects
@login_required
@permission_required('common.is_entrepreneur')
def my_projects_list(request):
	title = 'Mis proyectos'
	query_set = models.UserProject.objects.select_related('project').filter(user=request.user)
	projects = reversed(list(query_set))

	return render(request, 'common/project/my_projects_list.html', locals())

#Show call list to select one
@login_required
@permission_required('common.is_entrepreneur')
def my_projects_calls(request):
	title = 'Seleccione una Convocatoria a postular'
	today = datetime.date.today()
	query_set = models.Call.objects.select_related('entity').filter(due_date__gte=today)
	calls = reversed(list(query_set))
	context = {
		"title": title,
		"calls": calls,
	}
	return render(request, 'common/project/call_list.html', context)

#show entrepreneur profile
@login_required
@permission_required('common.is_entrepreneur')
def profile(request, user_id):
	title = 'Perfil Emprendedor'
	user = get_object_or_404(models.User, pk=user_id)
	profile = Profile.objects.select_related('user').get(user__id=user_id)
	if request.method == 'GET':
		return render(request, 'common/enterpreneur_profile/profile.html', locals())

#Edit a entrepreneur
@login_required
@permission_required('common.is_entrepreneur')
def update_profile(request, user_id):
	title = 'Editar Emprendedor'
	user = get_object_or_404(models.User, pk=user_id)
	profile = Profile.objects.select_related('user').get(user__id=user_id)
	if request.method == 'POST':
		form_profile = AccountForm(request.POST, request.FILES, instance = profile)
		form_user = UserForm(request.POST, instance = user)
		if form_profile.is_valid() and form_user.is_valid():
			user = form_user.save(commit = False)
			profile = form_profile.save(commit = False)
			user.save()
			profile.save()
			return redirect(reverse('common:entrepreneurhome'))
		else:
			print(form_profile.errors)
	else:
		form_profile = AccountForm(instance = profile)
		form_user = UserForm(instance = user)
		
	return render(request, 'common/enterpreneur_profile/update_profile.html', locals())

#Show call detail entrepreneur
@login_required
@permission_required('common.is_entrepreneur')
def my_project_call_detail(request, call_id):
	call = models.Call.objects.select_related('entity').get(pk=call_id)
	call_workshops = models.Workshop.objects.filter(call__id=call_id)
	context = {
		"call": call,
		"call_workshops": call_workshops,
	}
	
	return render(request, 'common/project/call_detail.html', context) 

#create users of type personal
@login_required
@permission_required('common.is_jaku_staff')
def create_personal(request):
	title = 'Agregar personal'
	if request.method == 'GET':
		return render(request, 'common/personal/form.html', locals())
	username = request.POST.get('email')
	if models.User.objects.filter(username=username):
		error = "Ya existe el usuario: " + username + "."			
		return render(request, 'common/personal/form.html', locals())
	
	group = Group.objects.get(name='Personal')
	
	pwd = request.POST.get('pwd')
	user = models.User(username=username, first_name=first_name, last_name=last_name, email=username)
	user.set_password(pwd)
	user.save()
	user.groups.add(group)
	return redirect(reverse('common:listpersonal'))

#edit users of type personal
@login_required
@permission_required('common.is_jaku_staff')
def edit_personal(request, personal_id):
	title = 'Editar personal'
	personal = get_object_or_404(models.User, pk=personal_id)
	if request.method == 'GET':
		return render(request, 'common/personal/edit.html', locals())
	username = request.POST.get('email')

	group = Group.objects.get(name='Personal')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	pwd = request.POST.get('pwd')
	if request.POST.get('password'):
		pwd = request.POST.get('password')
		personal.set_password(pwd)
	personal.first_name = first_name
	personal.last_name = last_name
	personal.email = username
	personal.username = username
	personal.groups.add(group)
	personal.save()
	return redirect(reverse('common:listpersonal'))

#shows all personal users as a list
@login_required
@permission_required('common.is_jaku_staff')
def personal_list(request):
	title = 'Lista de personal'
	query_set = models.User.objects.filter(groups__name='Personal')
	personal = reversed(list(query_set))
	return render(request, 'common/personal/list.html', locals())

#can delete a personal
@login_required
@permission_required('common.is_jaku_staff')
def delete_personal(request, personal_id):
	personal = get_object_or_404(models.User, pk=personal_id)
	personal.delete()
	return redirect(reverse('common:listpersonal'))

#create users of type jury
@login_required
@permission_required('common.is_jaku_staff')
def create_jury(request):
	title = 'Agregar jurado'
	if request.method == 'GET':
		return render(request, 'common/jury/form.html', locals())
	username = request.POST.get('email')
	if models.User.objects.filter(username=username):
		error = "Ya existe el usuario: " + username + "."			
		return render(request, 'common/jury/form.html', locals())
	
	group = Group.objects.get(name='Jurado')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	pwd = request.POST.get('pwd')
	phone_number = request.POST.get('phone_number')
	user = models.User(username=username, first_name=first_name, last_name=last_name, email=username)
	user.set_password(pwd)
	user.save()
	user.groups.add(group)
	jury = ProfileJury(user=user, phone_number=phone_number)
	jury.save()
	return redirect(reverse('common:listjury'))

#edit users of type jury
@login_required
@permission_required('common.is_jaku_staff')
def edit_jury(request, jury_id):
	title = 'Editar jurado'
	jury = ProfileJury.objects.select_related('user').get(pk=jury_id)
	user = jury.user
	if request.method == 'GET':
		return render(request, 'common/jury/edit.html', locals())
	username = request.POST.get('email')

	group = Group.objects.get(name='Jurado')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	pwd = request.POST.get('pwd')
	phone_number = request.POST.get('phone_number')
	if request.POST.get('password'):
		pwd = request.POST.get('password')
		user.set_password(pwd)
	user.first_name = first_name
	user.last_name = last_name
	user.email = username
	user.username = username
	user.groups.add(group)
	user.save()
	jury.phone_number = phone_number
	jury.user = user
	jury.save()
	return redirect(reverse('common:listjury'))

#shows all juries as a list
@login_required
@permission_required('common.is_jaku_staff')
def jury_list(request):
	title = 'Lista de jurados'
	query_set = ProfileJury.objects.select_related('user').all()
	juries = reversed(list(query_set))
	return render(request, 'common/jury/list.html', locals())

#can delete a jury
@login_required
@permission_required('common.is_jaku_staff')
def delete_jury(request, jury_id):
	jury = ProfileJury.objects.select_related('user').get(pk=jury_id)
	user = jury.user
	user.delete()
	jury.delete()
	return redirect(reverse('common:listjury'))

#create users of type mentor
@login_required
@permission_required('common.is_jaku_staff')
def create_mentor(request):
	title = 'Agregar mentor'
	if request.method == 'GET':
		return render(request, 'common/mentor/form.html', locals())
	username = request.POST.get('email')
	if models.User.objects.filter(username=username):
		error = "Ya existe el usuario: " + username + "."			
		return render(request, 'common/mentor/form.html', locals())
	
	group = Group.objects.get(name='Mentor')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	specialty = request.POST.get('specialty')
	pwd = request.POST.get('pwd')
	phone_number = request.POST.get('phone_number')
	user = models.User(username=username, first_name=first_name, last_name=last_name, email=username)
	user.set_password(pwd)
	user.save()
	user.groups.add(group)
	mentor = ProfileMentor(user=user, phone_number=phone_number, specialty=specialty)
	mentor.save()
	return redirect(reverse('common:listmentor'))

#edit users of type mentor
@login_required
@permission_required('common.is_jaku_staff')
def edit_mentor(request, mentor_id):
	title = 'Editar mentor'
	mentor = ProfileMentor.objects.select_related('user').get(pk=mentor_id)
	user = mentor.user
	if request.method == 'GET':
		return render(request, 'common/mentor/edit.html', locals())
	username = request.POST.get('email')

	group = Group.objects.get(name='Mentor')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	specialty = request.POST.get('specialty')
	pwd = request.POST.get('pwd')
	phone_number = request.POST.get('phone_number')
	if request.POST.get('password'):
		pwd = request.POST.get('password')
		user.set_password(pwd)
	user.first_name = first_name
	user.last_name = last_name
	user.email = username
	user.username = username
	user.groups.add(group)
	user.save()
	mentor.phone_number = phone_number
	mentor.specialty = specialty
	mentor.user = user
	mentor.save()
	return redirect(reverse('common:listmentor'))

#shows all mentors as a list
@login_required
@permission_required('common.is_jaku_staff')
def mentor_list(request):
	title = 'Lista de mentores'
	query_set = ProfileMentor.objects.select_related('user').all()
	mentors = reversed(list(query_set))
	return render(request, 'common/mentor/list.html', locals())

#can delete a mentor
@login_required
@permission_required('common.is_jaku_staff')
def delete_mentor(request, mentor_id):
	mentor = get_object_or_404(ProfileMentor, pk=mentor_id)
	user = mentor.user
	user.delete()
	mentor.delete()
	return redirect(reverse('common:listmentor'))

#create users of type coach
@login_required
@permission_required('common.is_jaku_staff')
def create_coach(request):
	title = 'Agregar coach'
	if request.method == 'GET':
		return render(request, 'common/coach/form.html', locals())
	username = request.POST.get('email')
	if models.User.objects.filter(username=username):
		error = "Ya existe el usuario: " + username + "."			
		return render(request, 'common/coach/form.html', locals())
	
	group = Group.objects.get(name='Coach')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	phone_number = request.POST.get('phone_number')
	pwd = request.POST.get('pwd')
	user = models.User(username=username, first_name=first_name, last_name=last_name, email=username)
	user.set_password(pwd)
	user.save()
	user.groups.add(group)
	coach = ProfileCoach(user=user, phone_number=phone_number)
	
	coach.save()
	return redirect(reverse('common:listcoach'))

#edit users of type coach
@login_required
@permission_required('common.is_jaku_staff')
def edit_coach(request, coach_id):
	title = 'Editar coach'
	coach = ProfileCoach.objects.select_related('user').get(pk=coach_id)
	user = coach.user
	if request.method == 'GET':
		return render(request, 'common/coach/edit.html', locals())
	username = request.POST.get('email')

	group = Group.objects.get(name='Coach')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	phone_number = request.POST.get('phone_number')
	pwd = request.POST.get('pwd')
	if request.POST.get('password'):
		pwd = request.POST.get('password')
		user.set_password(pwd)
	user.first_name = first_name
	user.last_name = last_name
	user.email = username
	user.username = username
	user.groups.add(group)
	user.save()
	coach.phone_number = phone_number
	coach.user = user
	coach.save()
	return redirect(reverse('common:listcoach'))

#shows all coach as a list
@login_required
@permission_required('common.is_jaku_staff')
def coach_list(request):
	title = 'Lista de coach'
	query_set = ProfileCoach.objects.select_related('user').all()
	coach = reversed(list(query_set))
	return render(request, 'common/coach/list.html', locals())

#can delete a coach
@login_required
@permission_required('common.is_jaku_staff')
def delete_coach(request, coach_id):
	coach = get_object_or_404(ProfileCoach, pk=coach_id)
	user = coach.user
	user.delete()
	coach.delete()
	return redirect(reverse('common:listcoach'))

#tmp
@login_required
def list_score_per_jury(request):
	title = 'Muestra los puntajes de los proyectos por jurado'
	projects = models.Project.objects.all()

	return render(request, 'common/score_per_jury/list.html', locals())

#tmp
@login_required
def jury_score_list(request, project_id):
	title = 'Puntajes por jurado'
	project = models.Project.objects.get(pk=project_id)
	score_project = EvaluationProject.objects.filter(project=project)

	return render(request, 'common/score_per_jury/score.html', locals())

#shows a list of existing preloaded workshops 
@login_required
@permission_required('common.is_jaku_staff')
def list_of_default_workshops(request):
	title = 'Talleres predeterminados'

	query_set = models.DefaultWorkshop.objects.all()
	defaultworkshops = reversed(list(query_set))
	return render(request, 'common/default_workshop/list.html', locals())


#can create a new preloaded workshop
@login_required
@permission_required('common.add_defaultworkshop')
def create_default_workshop(request):
	title = 'Agregar taller predeterminado'

	if request.method == 'GET':
		return render(request, 'common/default_workshop/form.html', locals())
	
	defaultworkshop_name = request.POST.get('name')
	defaultworkshop_description = request.POST.get('description')
	defaultworkshop_temary = request.POST.get('temary')
	defaultworkshop = models.DefaultWorkshop(name=defaultworkshop_name, description=defaultworkshop_description, temary=defaultworkshop_temary)
	defaultworkshop.save()
	return redirect('common:listofdefaultworkshops')

#can edit a preloaded workshop
@login_required
@permission_required('common.change_defaultworkshop')
def edit_default_workshop(request, default_workshop_id):
	title = 'Editar taller predeterminado'
	defaultworkshop = get_object_or_404(models.DefaultWorkshop, pk=default_workshop_id)

	if request.method == 'GET':
		return render(request, 'common/default_workshop/edit.html', locals())

	defaultworkshop_name = request.POST.get('name')
	defaultworkshop_description = request.POST.get('description')
	defaultworkshop_temary = request.POST.get('temary')
	defaultworkshop.name = defaultworkshop_name
	defaultworkshop.description = defaultworkshop_description
	defaultworkshop.temary = defaultworkshop_temary
	defaultworkshop.save()

	return redirect('common:listofdefaultworkshops')

#can delete a preloaded workshop
@login_required
@permission_required('common.delete_defaultworkshop')
def delete_default_workshop(request, default_workshop_id):
	defaultworkshop = get_object_or_404(models.DefaultWorkshop, pk=default_workshop_id)
	defaultworkshop.delete()
	
	return redirect('common:listofdefaultworkshops')
