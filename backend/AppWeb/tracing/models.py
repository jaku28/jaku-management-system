from django.db import models
from common.models import Call, Project
from accounts.models import ProfileMentor, ProfileJury

#Model for evaluation
class Evaluation(models.Model):
    class Meta:
        verbose_name = 'evaluación'
        verbose_name_plural = 'evaluaciones'

    call = models.ForeignKey(Call, on_delete=models.CASCADE, null=False, verbose_name='convocatoria')
    name = models.CharField('nombre', max_length=200)
    max_points = models.IntegerField('máximo de puntos', blank=False, null=False)
    date = models.DateField('fecha', null=False, blank=False)

    def __str__(self):
        return self.name

#Model for criteria in an evaluation
class Criteria(models.Model):
    class Meta:
        verbose_name = 'criterio'

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=False, verbose_name='evaluación')
    name = models.CharField('nombre', max_length=200)
    description = models.TextField('descripción', blank=False, null=False)
    weight = models.IntegerField('peso', blank=False, null=False)

    def __str__(self):
        return self.name

# Model for Mentoring
class Mentoring(models.Model):
    class Meta:
        verbose_name = 'mentoría'
    ATTENDED = (
				('1', 'PENDIENTE'),
				('2', 'ATENDIDO'),
                ('3', 'NO ATENDIDO'),
			)
    mentor = models.ForeignKey(ProfileMentor, on_delete=models.CASCADE, null=True, verbose_name='mentor')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    date = models.DateField('fecha', null=False, blank=False)
    time = models.TimeField(blank=True, null=True)
    is_attended = models.CharField('estado de la mentoría',choices=ATTENDED, max_length=1, null=False, default = '1')
    observations = models.TextField('observaciones del mentor')

#Relation between an evaluation and a jury
class EvaluationJury(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=False, verbose_name='evaluación')
    jury = models.ForeignKey(ProfileJury, on_delete=models.CASCADE, null=False, verbose_name='jurado')
    
    class Meta:
        unique_together = ('evaluation', 'jury',)

#Relation between criteria and project
class CriteriaProject(models.Model):
    jury = models.ForeignKey(ProfileJury, on_delete=models.CASCADE, null=False, verbose_name='jurado')
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE, null=False, verbose_name='criterio')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    point = models.IntegerField('puntaje', blank=False, null=False)    
        
#Relation between an evaluation and a project
class EvaluationProject(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=False, verbose_name='evaluacion')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    jury = models.ForeignKey(ProfileJury, on_delete=models.CASCADE, null=False, verbose_name='jurado')
    score = models.DecimalField('puntaje', blank=False, null=False, decimal_places=5, max_digits=10)

#Model for activity
class Activity(models.Model):
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    APPROVED = (
				('1', 'APROBADO A TIEMPO'),
				('2', 'APROBADO CON RETRASO'),
                ('3', 'APROBADO CON MUCHO RETRASO'),
			)

    title = models.CharField('título de la actividad', max_length=300)
    description = models.TextField('descripción de la actividad', blank=False, null=False)
    due_date = models.DateField('fecha límite', null=True, blank=True)
    file_activity = models.FileField('archivo adjunto de actividad', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    is_completed = models.BooleanField('completado', null=False, default = False)
    is_approved = models.CharField('aprobación de la actividad',choices=APPROVED, max_length=1, null=True)

#Points of a project in an evaluation
class EvaluationSummary(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=False, verbose_name='evaluación')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    final_score = models.DecimalField('puntaje', blank=True, null=True, decimal_places=5, max_digits=10)
    
class Interview(models.Model):
    class Meta:
        verbose_name = 'entrevista'
        verbose_name_plural = 'entrevistas'
    
    title = models.CharField('título', max_length=150, blank=False, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, verbose_name='proyecto')
    description = models.TextField('descripción', blank=False, null=True)
    link = models.CharField('link', max_length=200, null=True, blank=True)
    date = models.DateField('fecha', null=False, blank=False)
    time = models.TimeField('hora', blank=True, null=True)

    def __str__(self):
        return str(self.title)