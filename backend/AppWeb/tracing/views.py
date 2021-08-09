from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from common.models import Call, Project, UserProject
from .models import Mentoring, Evaluation, Criteria, EvaluationJury, CriteriaProject, EvaluationProject, Activity, EvaluationSummary
from .forms import *
from accounts.models import ProfileMentor, ProfileJury, ProfileCoach, User, Profile
import datetime
from common.email_utils import email_util
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import xlwt


#For creating a new evaluation
@login_required
def create_evaluation(request, call_id):
    title = 'Crear nueva evaluación'
    call = Call.objects.get(pk=call_id)

    if request.method == 'GET':
        return render(request, 'evaluation/form.html', locals())

    evaluation_name = request.POST.get('name')
    evaluation_date = request.POST.get('date')  
    evaluation_max_points = request.POST.get('max_points')
    
    evaluation = Evaluation(call=call, name=evaluation_name, date=evaluation_date, max_points=evaluation_max_points)
    evaluation.save()
    call.has_evaluations += 1
    call.save()

    if request.POST.get("save_evaluation"):
        return redirect('tracing:evaluationslist', call.id)
    else:
        return redirect('tracing:addcriteria', evaluation.id)

#Shows all evaluations of a call
@login_required
def show_evaluations(request, call_id):
    title = 'Lista de evaluaciones'
    call = Call.objects.get(pk=call_id)
    evaluations = Evaluation.objects.filter(call=call_id)

    return render(request, 'evaluation/list.html', locals())
    
#Edits an evaluation
@login_required 
def edit_evaluation(request, evaluation_id):
    title = 'Editar evaluación'
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    criterias = Criteria.objects.filter(evaluation=evaluation)

    if request.method == 'GET':
        return render(request, 'evaluation/edit.html', locals())

    evaluation_name = request.POST.get('name')
    evaluation_date = request.POST.get('date')
    evaluation_max_points = request.POST.get('max_points')

    criteria_name = request.POST.getlist('c_name')
    criteria_description = request.POST.getlist('c_description')
    criteria_weight = request.POST.getlist('c_weight')
    
    evaluation.name = evaluation_name
    evaluation.date = evaluation_date
    evaluation.max_points = evaluation_max_points
    evaluation.save()

    for c, cn, cd, cw in zip(criterias, criteria_name, criteria_description, criteria_weight):
        c.name = cn
        c.description = cd
        c.weight = cw
        c.save()

    return redirect('tracing:evaluationslist', evaluation.call.id)

#Shows evaluation detail
@login_required
def evaluation_detail(request, evaluation_id):
    title = 'Detalle de evaluación'
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    criterias = Criteria.objects.filter(evaluation=evaluation)
    return render(request, 'evaluation/detail.html', locals())

#Delete an evaluation
@login_required
def delete_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    call = evaluation.call
    evaluation.delete()
    call.has_evaluations -= 1
    call.save()
    
    return redirect('tracing:evaluationslist', evaluation.call.id)

#Adds criterias in an evaluation
@login_required
def add_criteria(request, evaluation_id):
    title = 'Criterios de evaluación'
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    
    if request.method == 'GET':
        return render(request, 'criteria/form.html', locals())

    criteria_names = request.POST.getlist('name')
    criteria_description = request.POST.getlist('description')
    criteria_weight = request.POST.getlist('weight')

    for n, d, w in zip(criteria_names, criteria_description, criteria_weight):
        criteria = Criteria(evaluation=evaluation, name=n, description=d, weight=w)
        criteria.save()

    return redirect('tracing:evaluationslist', evaluation.call.id)

#Shows all juries for an evaluation and edit juries
@login_required
@permission_required('tracing.change_evaluation')
def evaluation_juries(request, evaluation_id):
    title = 'Jurados'
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    evaluation_juries = EvaluationJury.objects.select_related('jury__user').filter(evaluation=evaluation_id)
    juries_already_added = []
    for evaluation_jury in evaluation_juries:
        juries_already_added.append(evaluation_jury.jury.pk)

    juries = ProfileJury.objects.select_related('user').exclude(id__in=juries_already_added)

    if request.method == 'GET':
        return render(request, 'evaluation_jury/list.html', locals())
    
    jury_id = request.POST.get('juries')
    jury = ProfileJury.objects.get(pk=jury_id)
 
    new_ej = EvaluationJury(evaluation=evaluation, jury=jury)
    new_ej.save()

    return redirect('tracing:evaluationjuries', evaluation.id) 

#Delete a jury from an evaluation
@login_required
@permission_required('tracing.change_evaluation')
def delete_evaluation_jury(request, ej_id):
    ej = get_object_or_404(EvaluationJury, pk=ej_id)
    evaluation = ej.evaluation
    ej.delete()
    return redirect('tracing:evaluationjuries', evaluation.id)

#List all the calls for a mentoring
@login_required
def list_calls(request):
	title = 'Convocatorias'
	query_set = Call.objects.all()
	calls = reversed(list(query_set))
	context = {
		"title": title,
		"calls": calls,
	}
	return render(request, 'mentoring/calls_list.html', context)

#List all the approved projects
def approved_projects(request, call_id):
    title = 'Proyectos Aprobados'
    leaders_ = []
    call = Call.objects.get(pk = call_id)
    query_set = Project.objects.select_related('call').filter(call=call).filter(is_approved = 2)
    for x in query_set:
        leader = Profile.objects.get(pk=x.leader)
        leaders_.append(leader)
    projects_approved = reversed(list(query_set))
    leaders = reversed(list(leaders_))
    return render(request, 'mentoring/projects_approved.html', locals())

#Show the mentoring list
def show_mentorings(request, project_id):
    title = 'Lista de Mentorías'
    project = Project.objects.select_related('call').get(pk=project_id)
    mentorings = Mentoring.objects.filter(project=project)
    today = datetime.date.today()

    return render(request, 'mentoring/list.html', locals())

#Create a new mentoring and notify the mentor
def create_mentoring(request, project_id):
    title = 'Crear nueva Mentoría'
    project = Project.objects.select_related('call').get(pk=project_id)
    mentors = ProfileMentor.objects.all()
    if request.method == 'GET':
        form = MentoringForm()
    else:
        form = MentoringForm(request.POST)
        if form.is_valid():
            mentoring = form.save(commit=False)
            mentoring.project = project
            mentoring.attended = 1
            mentoring.save()
            email_util().send_email_mentoring(request, mentoring)
            return redirect('tracing:showmentorings', project.id)
    return render(request, 'mentoring/form.html', locals())

#Edit a mentoring
def edit_mentoring(request, mentoring_id):
    title = 'Editar Mentoría'
    mentoring = get_object_or_404(Mentoring, pk=mentoring_id)
    project = mentoring.project
    mentors = ProfileMentor.objects.all()
    if request.method == 'GET':
        form = MentoringForm(instance = mentoring)
    else:
        form = MentoringForm(request.POST, instance = mentoring)
        if form.is_valid():
            mentoring = form.save(commit=False)
            mentoring.project = project
            mentoring.attended = 1
            mentoring.save()
            return redirect('tracing:showmentorings', project.id)
    return render(request, 'mentoring/edit.html', locals())

#delete an mentoring
@login_required
def delete_mentoring(request, mentoring_id):
    mentoring = get_object_or_404(Mentoring, pk=mentoring_id)
    project = mentoring.project
    mentoring.delete()
    
    return redirect('tracing:showmentorings', project.id)

#list all scheduled mentoring of a mentor
@login_required
def list_mentorings(request):
    title = 'Mis Mentorías'
    profile = ProfileMentor.objects.get(user=request.user)
    mentorings = Mentoring.objects.filter(mentor=profile)
    today = datetime.date.today()

    return render(request, 'mentor_data/list.html', locals())

#Mark attendance and add feedback in a mentoring
@login_required
def mark_attendance(request, mentoring_id):
    title = 'Observaciones'
    mentoring = get_object_or_404(Mentoring, pk=mentoring_id)
    today = datetime.date.today()
    if mentoring.date == today:
        if request.method == 'GET':
            return render(request, 'mentor_data/feedback.html', locals())
        mentoring.observations = request.POST.get('feedback')
        mentoring.is_attended = 2
        mentoring.save()
    
    return redirect('tracing:mentorhome')

#Mark absence in a mentoring
@login_required
def mark_absence(request, mentoring_id):
    mentoring = get_object_or_404(Mentoring, pk=mentoring_id)
    today = datetime.date.today()
    if mentoring.date == today:
        mentoring.is_attended = 3
        mentoring.save()
    
    return redirect('tracing:mentorhome')

#Shows evaluations assigned to a jury
@login_required
def get_jury_evaluations(request):
    title = 'Lista de evaluaciones'
    evaluations_ids = EvaluationJury.objects.values_list('evaluation').filter(jury__user__id=request.user.id)
    evaluations = Evaluation.objects.filter(id__in=evaluations_ids)
    today = datetime.date.today()

    return render(request, 'jury_data/evaluations_list.html', locals())

#Gets project evaluations for a jury
@login_required
def get_jury_projects(request, evaluation_id):
    title = 'Cartilla de evaluación' 
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    call_id = Evaluation.objects.values_list('call').get(id=evaluation_id)
    projects = Project.objects.filter(call=call_id)
    criterias = Criteria.objects.filter(evaluation__id=evaluation_id)

    return render(request, 'jury_data/projects_list.html', locals())

#Shows project detail for a jury
@login_required
def jury_project_detail(request, project_id):
    title = 'Detalle de proyecto'
    project = Project.objects.get(pk=project_id)

    return render(request, 'jury_data/project_detail.html', locals())

#Saves criterias points (evaluation points) for a project in an evaluation
@csrf_exempt
def save_evaluation_points_for_project(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    jury = ProfileJury.objects.get(user=request.user)
    project_id = received_json_data.get('p_id')
    project = Project.objects.get(pk=project_id)
    criteria_points = received_json_data.get('points')
    crit = Criteria.objects.get(pk=criteria_points[0].get('c'))
    evaluation = Evaluation.objects.get(pk=crit.evaluation.id) 
    num_juries_ids = EvaluationJury.objects.values_list('jury').filter(evaluation=evaluation)
    num_juries = num_juries_ids.count()

    sum = 0
    for cp in criteria_points:
        criteria_id = cp.get('c')
        criteria = Criteria.objects.get(pk=criteria_id)
        point = cp.get('point')
        criteria_score = int(point) * int(criteria.weight) *0.01
        sum = sum + criteria_score

        try:
            already_points = CriteriaProject.objects.get(criteria=criteria, project=project, jury=jury)
            already_points.point = point
            already_points.save()
        except CriteriaProject.DoesNotExist:
            criteria_points = CriteriaProject.objects.create(criteria=criteria, project=project, point=point, jury=jury)

    try: 
        already_project_jury_score = EvaluationProject.objects.get(evaluation=evaluation, project=project, jury=jury)
        already_project_jury_score.score = sum
        already_project_jury_score.save()
    except EvaluationProject.DoesNotExist:
        project_jury_score = EvaluationProject(evaluation=evaluation, project=project, jury=jury, score=sum) 
        project_jury_score.save()

    eval_project = EvaluationProject.objects.filter(project=project)

    total_sum_of_juries_score = 0
    for ep in eval_project:
        total_sum_of_juries_score = total_sum_of_juries_score + ep.score
    
    try:
        already_evaluation_summary = EvaluationSummary.objects.get(evaluation=evaluation, project=project)
        already_evaluation_summary.final_score = total_sum_of_juries_score/num_juries
        already_evaluation_summary.save()
    except EvaluationSummary.DoesNotExist:
        new_evaluation_summary = EvaluationSummary(evaluation=evaluation, project=project, final_score=total_sum_of_juries_score/num_juries)
        new_evaluation_summary.save()

    response_data = {}
    response_data['result'] = 'Guardado'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

#List all the active projects
@login_required
@permission_required('common.is_jaku_staff')
def active_projects(request, call_id):
    title = 'Proyectos vigentes'
    leaders_ = []
    call = Call.objects.get(pk = call_id)
    query_set= Project.objects.select_related('call').filter(call=call).filter(is_active = True)
    active_projects = reversed(list(query_set))
    return render(request, 'coach_assignment/active_projects.html', locals())

#Assign a coach to a project
@login_required
@permission_required('common.is_jaku_staff')
def assign_coach(request, project_id):
    title = 'Proyecto'
    project = Project.objects.get(pk = project_id)
    coaches = ProfileCoach.objects.select_related('user')
    if request.method == 'GET':
        return render(request, 'coach_assignment/assign_coach.html', locals())

    coach_id = request.POST.get('coaches')
    coach = ProfileCoach.objects.get(pk=coach_id)
    project.coach = coach
    project.save()
    email_util().send_email_coach(request, coach, project.name)
    return redirect('tracing:activeprojects', project.call.id)

#Shows projects assigned to a coach
@login_required
def coach_projects(request):
    title = 'Lista de proyectos'
    coach = ProfileCoach.objects.get(user=request.user)
    projects = Project.objects.select_related('call').filter(coach=coach)

    return render(request, 'coach_data/projects_list.html', locals())

#Shows activities of a project
@login_required
def list_activities(request, project_id):
    title = 'Actividades y mentorías'
    title_activity = 'Actividades asignadas'
    project = Project.objects.get(pk = project_id)
    query_activities = Activity.objects.filter(project=project)
    activities = reversed(list(query_activities))

    title_mentoring = 'Mentorías'
    query_mentorings = Mentoring.objects.select_related('mentor__user').filter(project=project)
    mentorings = reversed(list(query_mentorings))

    return render(request, 'coach_data/activities_list.html', locals())

#Create a new activity of a project
@login_required
@permission_required('tracing.add_activity')
def create_activity(request, project_id):
    title = 'Crear actividad'
    project = Project.objects.get(pk = project_id)
    if request.method == 'GET':
        form = ActivityForm()
    else:
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.project = project
            activity.save()
            return redirect('tracing:listactivities', project.id)
    return render(request, 'coach_data/form_activity.html', locals())

# Edit an activity
@login_required
@permission_required('tracing.change_activity')
def edit_activity(request, activity_id):
    title = 'Editar Actividad'
    activity = get_object_or_404(Activity, pk=activity_id)
    project = activity.project
    if request.method == 'GET':
        form = ActivityForm(instance = activity)
    else:
        form = ActivityForm(request.POST, request.FILES, instance = activity)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.project = project
            activity.save()
            return redirect('tracing:listactivities', project.id)
    return render(request, 'coach_data/edit_activity.html', locals())

#Delete an activity
@login_required
@permission_required('tracing.delete_activity')
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    project = activity.project
    activity.delete()
    
    return redirect('tracing:listactivities', project.id)

#Create global activities for all call's projects
@login_required
@permission_required('tracing.add_activity')
def global_activity(request, call_id):
    title = 'Crear actividad global'
    call = Call.objects.get(pk = call_id)
    projects = Project.objects.select_related('call').filter(call=call).filter(is_active = True)

    if request.method == 'GET':
        form = ActivityForm()
    else:
        title_ = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        for p in projects:
            activity = Activity(project = p, title = title_, description = description, due_date = due_date)
            activity.save()
        return redirect('tracing:activeprojects', call.id)
    return render(request, 'coach_assignment/form_activity.html', locals())

#Shows activities of a project
@login_required
@permission_required('common.is_entrepreneur')
def project_activities(request, project_id):
    title = 'Actividades y mentorías'
    title_activity = 'Actividades asignadas'
    project = Project.objects.get(pk = project_id)
    query_activities = Activity.objects.filter(project=project)
    activities = reversed(list(query_activities))

    title_mentoring = 'Mentorías'
    query_mentorings = Mentoring.objects.select_related('mentor__user').filter(project=project)
    mentorings = reversed(list(query_mentorings))

    return render(request, 'activity/activities_list.html', locals())

#Complete an activity sending a file
@login_required
@permission_required('common.is_entrepreneur')
def complete_activity(request, activity_id):
    title = 'Completar actividad'
    activity = Activity.objects.get(pk=activity_id)
    if activity.is_completed == False:
        if request.method == 'GET':
            return render(request, 'activity/complete.html', locals())
        
        activity.file_activity = request.FILES['file']
        activity.is_completed = True
        activity.save()
    return redirect('tracing:projectactivities', activity.project.id)

#Check an activity
@login_required
def check_activity(request, activity_id):
    title = 'Revisar actividad'
    activity = Activity.objects.get(pk=activity_id)
    return render(request, 'coach_data/check_activity.html', locals())

#Approve an activity
@login_required
def aprrove_activity(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if not activity.is_approved:
        today = datetime.date.today()
        if activity.due_date >= today:
            activity.is_approved = 1
        else:
            if (today - activity.due_date).days == 1:
                
                activity.is_approved = 2
            else:
                activity.is_approved = 3
        activity.save()
    return redirect('tracing:listactivities', activity.project.id)

#Reject an activity
@login_required
def reject_activity(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if not activity.is_approved:
        activity.is_completed = False
        activity.save()
    return redirect('tracing:listactivities', activity.project.id)

#Shows calls as a lisgt for evaluation data in admin
@login_required
@permission_required('common.is_jaku_staff')  
def evaluation_calls_list(request):
    title = 'Lista de convocatorias'
    today = datetime.date.today()
    calls = Call.objects.filter(due_date__lt= today)
    #Search
    queryset = request.GET.get("buscar")
    if queryset:
        calls = Call.objects.filter(
            Q(name__icontains = queryset) |
            Q(entity_id__name__icontains = queryset)
        ).distinct()
    #Pagination    
    paginator = Paginator(calls,5)
    page = request.GET.get('page')
    calls = paginator.get_page(page)

    return render(request, 'evaluations_data/calls_list.html', locals()) 

#Shows evaluations list from a call in evaluation data in admin
@login_required
@permission_required('common.is_jaku_staff')
def eval_evaluations_list(request, call_id):
    title = 'Lista de evaluaciones'
    evaluations = Evaluation.objects.filter(call__id=call_id)

    return render(request, 'evaluations_data/evaluations_list.html', locals()) 

#Shows juries list for evaluation cards in evaluation data in admin
@login_required
@permission_required('common.is_jaku_staff')
def evaluations_cards(request, evaluation_id):
    title = 'Cartillas de evaluación por jurado'
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    juries_ids = EvaluationJury.objects.values_list('jury').filter(evaluation=evaluation)
    juries = ProfileJury.objects.select_related('user').filter(pk__in=juries_ids)

    return render(request, 'evaluations_data/evaluations_cards_list.html', locals())

#Shows evaluation card of a jury in evaluation data in admin
@login_required
@permission_required('common.is_jaku_staff')
def admin_evaluation_card(request, evaluation_id, jury_id):
    title = 'Cartilla de evaluación'
    jury = ProfileJury.objects.select_related('user').get(pk=jury_id)
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    projects = Project.objects.filter(call=evaluation.call)
    criterias = Criteria.objects.filter(evaluation=evaluation)
    criteria_projects = CriteriaProject.objects.select_related('criteria','project').filter(project__in=projects, jury=jury)
    
    for p in projects:
        p.criteria_projects = []
        for cp in criteria_projects:
            if cp.project == p:
                p.criteria_projects.append(cp)

    points_registered_dict = {}
    for cp in criteria_projects:
        key = str(cp.project.id) + '-' + str(cp.criteria.id)
        points_registered_dict[key] = cp.point

    return render(request, 'evaluations_data/evaluation_card.html', locals())

#Shows projects ranking of an evaluation
@login_required
@permission_required('common.is_jaku_staff')
def projects_ranking(request, evaluation_id):
    title = 'Ranking de proyectos'
    evaluation = Evaluation.objects.select_related('call').get(pk=evaluation_id)
    call_id = Call.objects.values_list('pk').get(pk=evaluation.call.id) 
    projects = Project.objects.filter(call=call_id).filter(is_active=True)
    score_per_juries = EvaluationProject.objects.select_related('project','jury').filter(evaluation=evaluation)
    juries_id = EvaluationJury.objects.values_list('jury__id').filter(evaluation=evaluation)
    juries = ProfileJury.objects.select_related('user').filter(id__in=juries_id)
    final_scores = EvaluationSummary.objects.select_related('project').filter(evaluation=evaluation)
    
    final_score_dict = {}
    for fc in final_scores:
        key_fc = str(fc.project.id)
        final_score_dict[key_fc] = fc.final_score 
    
    for p in projects:
        value = final_score_dict.get(str(p.id))
        p.eval_score = value
        p.save()

    projects = projects.order_by('-eval_score')
    
    for p in projects:
        p.score_per_juries = []
        for sc in score_per_juries:
            if sc.project == p:
                p.score_per_juries.append(sc)

    points_per_jury_dict = {}
    for sc in score_per_juries:
        key = str(sc.project.id) + '-' + str(sc.jury.id)
        points_per_jury_dict[key] = sc.score

    return render(request, 'evaluations_data/projects_ranking.html', locals())

#Add umbral
@login_required
@permission_required('common.is_jaku_staff')
def add_umbral(request, evaluation_id):
    title = 'Agregar umbral'
    evaluation = Evaluation.objects.select_related('call').get(pk=evaluation_id)
    call_id = Call.objects.values_list('pk').get(pk=evaluation.call.id) 
    projects = Project.objects.filter(call=call_id)
    
    if request.method == 'GET':
        return render(request, 'evaluations_data/umbral.html', locals())

    umbral = request.POST.get('umbral')
    for p in projects:
        if p.eval_score >= float(umbral):
            p.is_active = True
            p.save()
        else:
            p.is_active = False
            p.save()

    return redirect('tracing:projectsranking', evaluation.id)

#Block a project in active project list
@login_required
@permission_required('common.is_jaku_staff')
def block_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.is_active = False
    project.save()
    
    return redirect('tracing:activeprojects', project.call.id)

#Exports evaluation card of a jury in evaluation data in admin     
@login_required
@permission_required('common.is_jaku_staff')
def export_evaluation_card(request, evaluation_id, jury_id):
    title = 'Cartilla de evaluación'
    jury = ProfileJury.objects.select_related('user').get(pk=jury_id)
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    projects = Project.objects.filter(call=evaluation.call)
    criterias = Criteria.objects.filter(evaluation=evaluation)
    criteria_projects = CriteriaProject.objects.select_related('criteria','project').filter(project__in=projects, jury=jury)
    
    for p in projects:
        p.criteria_projects = []
        for cp in criteria_projects:
            if cp.project == p:
                p.criteria_projects.append(cp)

    response = HttpResponse(content_type='application/ms-excel')
    filename = 'cartilla_' + evaluation.name + '_' + jury.user.last_name + '_' + jury.user.first_name + '.xls'
    rp = 'attachment; filename=' + str(filename)
    response['Content-Disposition'] = rp
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(title)

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    title_sheet = title + ' de: ' + jury.user.last_name + ', ' + jury.user.first_name
    ws.write(row_num, 0, title_sheet, font_style)
    
    row_num += 1
    name = 'Evaluación: ' + evaluation.name
    ws.write(row_num, 0, name, font_style)

    row_num += 1
    scale = 'Escala de puntuación: 1 - ' + str(evaluation.max_points)
    ws.write(row_num, 0, scale, font_style)
    
    row_num += 1
    column_num = 0
    ws.write(row_num, column_num, 'Proyecto', font_style)
    for c in criterias:
        column_num += 1
        criteria = c.name + ' - ' + c.description + ' - ' + str(c.weight) + '%'
        ws.write(row_num, column_num, criteria, font_style)

    font_style = xlwt.XFStyle()
    for p in projects:
        row_num += 1
        column_num = 0
        ws.write(row_num, column_num, p.name, font_style)
        for cp in p.criteria_projects:
            column_num += 1
            ws.write(row_num, column_num, str(cp.point), font_style)

    wb.save(response)
    return response

#Create a interview of a project
@login_required
@permission_required('tracing.add_interview')
def create_interview(request, project_id):
    title = 'Crear entrevista'
    project = Project.objects.get(pk = project_id)
    if request.method == 'GET':
        form = InterviewForm()
    else:
        form = InterviewForm(request.POST, request.FILES)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.project = project
            interview.save()
            return redirect('tracing:activeprojects', project.call_id)
    return render(request, 'interview/form_interview.html', locals())