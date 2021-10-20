from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from accounts.models import ProfileCoach

class Entity(models.Model):
	class Meta:
		verbose_name = 'entidad'
		verbose_name_plural = 'entidades'

	name = models.CharField('nombre', max_length=200)

	def __str__(self):
		return self.name

class Call(models.Model):
	class Meta:
		ordering = ['id']
		verbose_name = 'convocatoria'
		permissions = (
				('is_jaku_staff', 'Is a Jaku staff'),
		)

	name = models.CharField('título', max_length=300)
	num_projects = models.IntegerField(default=1)
	has_projects = models.IntegerField(default=0)
	has_evaluations = models.IntegerField(default=0)
	entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, verbose_name='entidad')
	due_date = models.DateField('fecha límite', null=True, blank=True)
	preparation_start = models.DateField('fecha de inicio de prepación para equipos', null=True, blank=True)
	final_date = models.DateField('fecha final', null=True, blank=True)
	award = models.CharField('premio', max_length=50)
	rules = models.FileField('bases')
	is_reviewed = models.BooleanField(default=False)
	is_incubation = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Project(models.Model):
	class Meta:
		verbose_name = 'proyecto'
		permissions = (
				('is_entrepreneur', 'Is an entrepreneur'),
		)
	PROJECT_TYPE = (
				('1', 'BASE TECNOLÓGICA'),
				('2', 'SOCIAL'),
				('3', 'PRODUCTIVO'),
			)

	PROJECT_APPROVAL = (
				('1', 'PENDIENTE'),
				('2', 'APROBADO'),
				('3', 'RECHAZADO'),
			)
	
	LOCATION = (
		('1', 'AMAZONAS'),
		('2', 'ANCASH'),
		('3', 'APURIMAC'),		
		('4', 'AREQUIPA'),
		('5', 'AYACUCHO'),
		('6', 'CAJAMARCA'),
		('7', 'CALLAO'),
		('8', 'CUSCO'),
		('9', 'HUANCAVELICA'),
		('10', 'HUANUCO'),
		('11', 'ICA'),
		('12', 'JUNIN'),
		('13', 'LA LIBERTAD'),
		('14', 'LAMBAYEQUE'),
		('15', 'LIMA'),
		('16', 'LORETO'),
		('17', 'MADRE DE DIOS'),
		('18', 'MOQUEGUA'),
		('19', 'PASCO'),
		('20', 'PIURA'),
		('21', 'PUNO'),
		('22', 'SAN MARTIN'),
		('23', 'TACNA'),
		('24', 'TUMBES'),
		('25', 'UCAYALI'),
	) 
	
	code = models.CharField('codigo del emprendimiento', max_length=100, null=True)
	leader = models.IntegerField(verbose_name='id lider de proyecto')
	name = models.CharField('título del emprendimiento', max_length=300)
	call = models.ForeignKey(Call, on_delete=models.CASCADE, null=True, verbose_name='convocatoria')
	location = models.CharField('ubicación', choices=LOCATION, max_length=2)
	project_type = models.CharField('tipo de proyecto',choices=PROJECT_TYPE, max_length=1)
	summary = models.TextField('resumen del emprendimiento', blank=False, null=False)
	detail_description = models.TextField('descripción a detalle del emprendimiento', blank=False, null=False)
	detail_market_needs = models.TextField('justificación basado en necesidad del mercado', blank=False, null=False)
	members = models.TextField('miembros del equipo')
	link_video = models.CharField('link', max_length=200, null=True, blank=True)
	is_approved = models.CharField('estado del proyecto',choices=PROJECT_APPROVAL, max_length=1, null=False, default = '1')
	is_active = models.BooleanField('activo', null=False, default = True)
	coach = models.ForeignKey(ProfileCoach, on_delete=models.CASCADE, null=True, blank=True, verbose_name='coach')
	eval_score = models.DecimalField('puntaje temporal de evaluacion', blank=True, null=True, decimal_places=5, max_digits=10)
	budget = models.CharField('presupuesto', max_length=50)

	def __str__(self):
		return self.name

class BudgetRegistry(models.Model):
	description = models.CharField('descripción', max_length=100, null=True)
	actual_budget = models.IntegerField(verbose_name='presupuesto')
	project = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return self.description

class BigForm(models.Model):
	class Meta:
		verbose_name = 'bigForm'
	
	field0 = models.CharField('campo0', max_length=200, null=True, blank=True)
	field1 = models.CharField('campo1', max_length=200, null=True, blank=True)
	field2 = models.CharField('campo2', max_length=200, null=True, blank=True)
	field3 = models.CharField('campo3', max_length=200, null=True, blank=True)
	field4 = models.CharField('campo4', max_length=200, null=True, blank=True)
	field5 = models.CharField('campo5', max_length=200, null=True, blank=True)
	field6 = models.FileField('campo6', max_length=200, null=True, blank=True)
	field7 = models.FileField('campo7', max_length=200, null=True, blank=True)
	field8 = models.FileField('campo8', max_length=200, null=True, blank=True)
	field9 = models.FileField('campo9', max_length=200, null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)


class FormConfig(models.Model):
	class Meta:
		verbose_name = 'formConfig'

	field = models.CharField('campo', max_length=200)
	type = models.CharField('tipo', max_length=200)
	label = models.CharField('etiqueta', max_length=200)
	call = models.ForeignKey(Call, on_delete=models.CASCADE)


	def __str__(self):
		return self.field


class UserProject(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='usuario')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, verbose_name='proyecto')

class New(models.Model):
	class Meta:
		verbose_name = 'noticia'

	title = models.CharField('título', max_length=200, blank=False, null=True)
	description = models.TextField('descripción', blank=False, null=True)
	image = models.ImageField('imagen', null=True)

	def __str__(self):
		return self.title

class Event(models.Model):
	class Meta:
		verbose_name = 'evento'

	def validate_date(date):
		if date < timezone.now().date():
			raise ValidationError("Date cannot be in the past")
				
	title = models.CharField('título', max_length=200, blank=False, null=True)
	description = models.TextField('descripción', blank=False, null=True)
	date = models.DateField('fecha', null=True, blank=True, validators=[validate_date])
	image = models.ImageField('imagen', null=True)
	link = models.CharField('link', max_length=150, null=True, blank=True)

	def __str__(self):
		return str(self.title)

	

class EventRegister(models.Model):
	class Meta:
		verbose_name = 'registro a evento'
		verbose_name_plural = 'registros a eventos'

	event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, verbose_name='evento')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='usuario')

class DefaultTask(models.Model):
	class Meta:
		verbose_name = 'tarea precargada'
		verbose_name_plural = 'tareas precargadas'

	name = models.CharField('nombre', max_length=150, blank=False, null=True)

	def __str__(self):
		return str(self.name)

class Task(models.Model):
	class Meta:
		verbose_name = 'tarea'
		permissions = (
				('mark_as_done_task', 'Can mark  a task as done'),
			)

	name = models.CharField('nombre', max_length=150, blank=False, null=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='evento') 
	assigned_date = models.DateField('fecha de asignación', null=True, blank=True) 
	due_date = models.DateField('fecha limite', null=True, blank=True) 
	assign_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='asignado a')
	is_done = models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)

class DefaultWorkshop(models.Model):
	class Meta:
		verbose_name = 'taller predeterminado'
		verbose_name_plural = 'talleres predeterminados'

	name = models.CharField('nombre', max_length=150, blank=False, null=True)
	description = models.TextField('descripción', blank=False, null=True)
	temary = models.TextField('temario', blank=False, null=True)

	def __str__(self):
		return str(self.name)

class Workshop(models.Model):
	class Meta:
		verbose_name = 'taller'
		verbose_name_plural = 'talleres'

	name = models.CharField('nombre', max_length=150, blank=False, null=True)
	call = models.ForeignKey(Call, on_delete=models.CASCADE, verbose_name='convocatoria')
	description = models.TextField('descripción', blank=False, null=True)
	temary = models.TextField('temario', blank=False, null=True)

	def __str__(self):
		return str(self.name)