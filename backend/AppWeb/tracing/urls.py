from django.urls import include, path
from . import views

app_name = 'tracing'
urlpatterns = [

	path('mentor/', views.list_mentorings, name='mentorhome'),
	path('mentor/inasistencia/<int:mentoring_id>/', views.mark_absence, name='markabsence'),
	path('mentor/observaciones/<int:mentoring_id>/', views.mark_attendance, name='markattendance'),
	
	path('convocatoria/evaluaciones/agregar/<int:call_id>/', views.create_evaluation, name='createevaluation'),
	path('convocatoria/evaluaciones/detalle/<int:evaluation_id>/', views.evaluation_detail, name='evaluationdetail'),
	path('convocatoria/evaluaciones/editar/<int:evaluation_id>/', views.edit_evaluation, name='editevaluation'),
	path('convocatoria/evaluaciones/eliminar/<int:evaluation_id>/', views.delete_evaluation, name='deleteevaluation'),
	path('convocatoria/evaluaciones/<int:call_id>/', views.show_evaluations, name='evaluationslist'),
	path('convocatoria/evaluaciones/agregar/criterios/<int:evaluation_id>/', views.add_criteria, name='addcriteria'),
	path('convocatoria/evaluaciones/jurados/<int:evaluation_id>/', views.evaluation_juries, name='evaluationjuries'),
	path('convocatoria/evaluaciones/jurados/eliminar/<int:ej_id>/', views.delete_evaluation_jury, name='deleteevaluationjury'),

	path('mentoria/convocatorias/', views.list_calls, name='listcalls'),
	path('mentoria/convocatorias/<int:call_id>/', views.approved_projects, name='approvedprojects'),
	path('mentoria/convocatorias/proyectos/<int:project_id>/', views.show_mentorings, name='showmentorings'),
	path('mentoria/convocatorias/proyectos/agregar/<int:project_id>/', views.create_mentoring, name='creatementoring'),
	path('mentoria/convocatorias/proyectos/editar/<int:mentoring_id>/', views.edit_mentoring, name='editmentoring'),
	path('mentoria/convocatorias/proyectos/eliminar/<int:mentoring_id>/', views.delete_mentoring, name='deletementoring'),

	path('mis-evaluaciones/', views.get_jury_evaluations, name='juryhome'),
	path('mis-evaluaciones/cartilla-evaluacion/<int:evaluation_id>/', views.get_jury_projects, name='getjuryprojects'),
	path('mis-evaluaciones/cartilla-evaluacion/save/', views.save_evaluation_points_for_project, name='saveevaluationpointsforproject'),
	path('mis-evaluaciones/detalle-proyecto/<int:project_id>/', views.jury_project_detail, name='juryprojectdetail'),

	path('proyectos-asignados/', views.coach_projects, name='coachhome'),
	path('proyectos-asignados/actividades/<int:project_id>/', views.list_activities, name='listactivities'),
	path('proyectos-asignados/actividades/agregar/<int:project_id>/', views.create_activity, name='createactivity'),
	path('proyectos-asignados/actividades/editar/<int:activity_id>/', views.edit_activity, name='editactivity'),
	path('proyectos-asignados/actividades/eliminar/<int:activity_id>/', views.delete_activity, name='deleteactivity'),
	path('proyectos-asignados/actividades/revisar/<int:activity_id>/', views.check_activity, name='checkactivity'),
	path('proyectos-asignados/actividades/aprobar/<int:activity_id>/', views.aprrove_activity, name='approveactivity'),
	path('proyectos-asignados/actividades/rechazar/<int:activity_id>/', views.reject_activity, name='rejectactivity'),

	path('mis-actividades/<int:project_id>/', views.project_activities, name='projectactivities'),
	path('mis-actividades/completar/<int:activity_id>/', views.complete_activity, name='completeactivity'),

	path('evaluacion-lista-convocatorias/', views.evaluation_calls_list, name='evaluationcallslist'),
	path('evaluacion-lista-convocatorias/evaluaciones/<int:call_id>/', views.eval_evaluations_list, name='evalevaluationslist'),
	path('evaluacion-lista-convocatorias/evaluaciones/ranking/<int:evaluation_id>/', views.projects_ranking, name='projectsranking'),
	path('evaluacion-lista-convocatorias/evaluaciones/ranking/umbral/<int:evaluation_id>/', views.add_umbral, name='addumbral'),
	path('evaluacion-lista-convocatorias/evaluaciones/cartillas-evaluacion/<int:evaluation_id>/', views.evaluations_cards, name='evaluationscards'),
	path('evaluacion-lista-convocatorias/evaluaciones/cartillas-evaluacion/detalle/<int:evaluation_id>/<int:jury_id>/', views.admin_evaluation_card, name='adminevaluationcard'),
	path('evaluacion-lista-convocatorias/evaluaciones/cartillas-evaluacion/detalle/descargar/<int:evaluation_id>/<int:jury_id>/', views.export_evaluation_card, name='exportevaluationcard'),
	
	path('evaluacion-lista-convocatorias/proyectos-vigentes/<int:call_id>/', views.active_projects, name='activeprojects'),
	path('evaluacion-lista-convocatorias/proyectos-vigentes/agregar-actividad/<int:call_id>/', views.global_activity, name='globalactivity'),
	path('evaluacion-lista-convocatorias/proyectos-vigentes/asignar-coach/<int:project_id>/', views.assign_coach, name='assigncoach'),
	path('evaluacion-lista-convocatorias/proyectos-vigentes/bloquear-proyecto/<int:project_id>/', views.block_project, name='blockproject'),

	path('evaluacion-lista-convocatorias/proyectos-vigentes/entrevista/agregar/<int:project_id>/', views.create_interview, name='createinterview'),

]
