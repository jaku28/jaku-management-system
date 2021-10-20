from django.urls import include, path
from . import views
from .views import show_news, create_news, edit_news, delete_news

app_name = 'common'
urlpatterns = [
	
	path('', views.system_home, name='home'),
	path('administrador/', views.show_calls, name='adminhome'),
	path('emprendedor/', views.e_show_events, name='entrepreneurhome'),
	
	path('registro/', views.entrepreneur_registry, name='entrepreneurregistry'),
	
	path('evento/', views.create_event, name='createevent'),
	path('evento/<int:event_id>/', views.event_detail, name='eventdetail'),
	path('evento/lista/', views.show_events, name='eventlist'),
	path('evento/tareas-precargadas/<int:event_id>/', views.show_default_tasks, name='defaulttasklist'),
	path('evento/nueva-tarea/<int:event_id>/', views.update_event, name='updateevent'),
	path('evento/editar/<int:event_id>/', views.edit_event, name='editevent'),
	path('evento/editar/tareas/<int:event_id>/', views.edit_event_tasks, name='editeventtasks'),
	path('evento/edit/tareas/eliminar/<int:event_id>/<int:task_id>/', views.delete_event_task, name='deleteeventtask'),
	path('evento/eliminar/<int:event_id>/', views.delete_event, name='deleteevent'),
	path('evento/lista-de-asistentes/<int:event_id>', views.attendee_list, name='attendeelist'),
	path('evento/lista-de-asistentes/descargar/<int:event_id>', views.export, name='export'),

	path('usuario/', views.user_list, name='userlist'),
	path('usuario/<int:user_id>/', views.user_detail, name='userdetail'),
	path('usuario/agregar/', views.create_user, name='createuser'),
	path('usuario/editar/<int:user_id>/', views.edit_user, name='edituser'),
	path('usuario/eliminar/<int:user_id>/', views.delete_user, name='deleteuser'),	

	path('solicitudes/', views.request_list, name='requestlist'),
	path('solicitudes/<int:r_id>/', views.request_detail, name='requestdetail'),
	path('solicitudes/aceptar/<int:r_id>/', views.accept_entrepreneur, name='acceptentrepreneur'),
	path('solicitudes/rechazar/<int:r_id>/', views.reject_entrepreneur, name='rejectentrepreneur'),

	path('tarea-precargada/', views.list_of_default_tasks, name='listofdefaulttasks'),
	path('tarea-precargada/agregar/', views.create_default_task, name='createdefaulttask'),
	path('tarea-precargada/editar/<int:default_task_id>/', views.edit_default_task, name='editdefaulttask'),
	path('tarea-precargada/eliminar/<int:default_task_id>/', views.delete_default_task, name='deletedefaulttask'),	

	path('taller-predeterminado/', views.list_of_default_workshops, name='listofdefaultworkshops'),
	path('taller-predeterminado/agregar/', views.create_default_workshop, name='createdefaultworkshop'),
	path('taller-predeterminado/editar/<int:default_workshop_id>/', views.edit_default_workshop, name='editdefaultworkshop'),
	path('taller-predeterminado/eliminar/<int:default_workshop_id>/', views.delete_default_workshop, name='deletedefaultworkshop'),

	path('noticia/', show_news, name='new'),
	path('noticia/agregar/', create_news, name='createnew'),
	path('noticia/editar/<int:new_id>', edit_news, name='editnew'),
	path('noticia/eliminar/<int:new_id>', delete_news, name='deletenew'),

	path('convocatoria/', views.create_call, name='createcall'),
	path('convocatoria/lista/', views.show_calls, name='calllist'),
	path('convocatoria/talleres-predeterminados/<int:call_id>/', views.show_default_workshops, name='defaultworkshoplist'),
	path('convocatoria/nuevo-taller/<int:call_id>/', views.edit_call, name='editcall'),
	path('convocatoria/editar/talleres/<int:call_id>/', views.edit_call_workshops, name='editcallworkshops'),
	path('convocatoria/edit/talleres/eliminar/<int:call_id>/<int:workshop_id>/', views.delete_call_workshop, name='deletecallworkshop'),
	path('convocatoria/<int:call_id>/', views.call_detail, name='calldetail'),
	path('convocatoria/editar/<int:call_id>/', views.update_call, name='updatecall'),
	path('convocatoria/eliminar/<int:call_id>/', views.delete_call, name='deletecall'),
	path('convocatoria/proyectos/<int:call_id>/', views.call_projects_list, name='callprojectslist'),	
	path('convocatoria/proyectos/detalle/<int:call_id>/<int:project_id>/', views.call_project_detail, name='callprojectdetail'),
	path('convocatoria/proyectos/detalle/aprobar/<int:project_id>/', views.approve_project, name='approveproject'),
	path('convocatoria/proyectos/detalle/rechazar/<int:project_id>/', views.reject_project, name='rejectproject'),
	path('convocatoria/proyectos/terminar/<int:call_id>/', views.finish_review, name='finishreview'),	

	path('entidad/', views.list_of_entities, name='listofentities'),
	path('entidad/agregar/', views.create_entity, name='createentity'),
	path('entidad/editar/<int:entity_id>/', views.edit_entity, name='editentity'),

	path('tareas-asignadas/', views.show_my_assigned_tasks, name='showmyassignedtasks'),
	path('tareas-asignadas/marcar/<int:task_id>', views.mark_as_done, name='markasdone'),
	path('tareas-asignadas/desmarcar/<int:task_id>', views.mark_as_not_done, name='markasnotdone'),

	path('eventos/', views.e_show_events, name='e_showevents'),
	path('eventos/mis-eventos/', views.e_show_my_events, name='e_show_myevents'),
	path('eventos/registrarme/<int:event_id>', views.register, name='register'),
	path('eventos/anular-registro/<int:event_id>', views.leave, name='leave'),

	path('mis-proyectos/', views.my_projects_list, name='myprojectslist'),
	path('mis-proyectos/<int:project_id>/', views.my_project_detail, name='myprojectdetail'),
	path('mis-proyectos/convocatorias/', views.my_projects_calls, name='myprojectscalls'),
	path('mis-proyectos/agregar/<int:call_id>', views.create_project, name='createproject'),
	path('mis-proyectos/editar/<int:project_id>/', views.edit_project, name='editproject'),
	path('mis-proyectos/eliminar/<int:project_id>/', views.delete_project, name='deleteproject'),
	path('mis-proyectos/detalle-de-convocatoria/<int:call_id>/', views.my_project_call_detail, name='myprojectcalldetail'),
	path('mis-proyectos/financieros/<int:project_id>/', views.my_project_budget, name='myprojectbudget'),
	path('mis-proyectos/editar/financieros/<int:project_id>/', views.edit_project_budget, name='editprojectbudget'),
	path('mis-proyectos/eliminar/financieros/<int:project_id>/<int:budget_registry_id>/', views.delete_project_budget, name='deleteprojectbudget'),

	path('perfil/<int:user_id>/', views.profile, name='profile'),
	path('perfil/editar/<int:user_id>/', views.update_profile, name='update_profile'),

	path('personal/', views.personal_list, name='listpersonal'),
	path('personal/editar/<int:personal_id>/', views.edit_personal, name='editpersonal'),
	path('personal/agregar/', views.create_personal, name='createpersonal'),
	path('personal/eliminar/<int:personal_id>/', views.delete_personal, name='deletepersonal'),

	path('jurado/', views.jury_list, name='listjury'),
	path('jurado/editar/<int:jury_id>/', views.edit_jury, name='editjury'),
	path('jurado/agregar/', views.create_jury, name='createjury'),
	path('jurado/eliminar/<int:jury_id>/', views.delete_jury, name='deletejury'),

	path('mentores/', views.mentor_list, name='listmentor'),
	path('mentores/editar/<int:mentor_id>/', views.edit_mentor, name='editmentor'),
	path('mentores/agregar/', views.create_mentor, name='creatementor'),
	path('mentores/eliminar/<int:mentor_id>/', views.delete_mentor, name='deletementor'),

	path('coach/', views.coach_list, name='listcoach'),
	path('coach/editar/<int:coach_id>/', views.edit_coach, name='editcoach'),
	path('coach/agregar/', views.create_coach, name='createcoach'),
	path('coach/eliminar/<int:coach_id>/', views.delete_coach, name='deletecoach'),
	path('coach/restaurar/<int:coach_id>/', views.restore_coach, name='restorecoach'),
	
	#tmp
	path('lista-puntaje-por-jurado/', views.list_score_per_jury, name='listscoreperjury'),
	path('lista-puntaje-por-jurado/score/<int:project_id>/', views.jury_score_list, name='juryscorelist'),
]