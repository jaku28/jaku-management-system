from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .helpers import profile_image_path
from django.core.validators import RegexValidator

#An extension of user model
class Profile(models.Model):
    SEX_CHOICES = (
        ('F', 'Femenino',),
        ('M', 'Masculino',),
        ('N', 'No especifica',),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=profile_image_path, default='defaults/img/default-user.png')
    dni = models.CharField('dni', max_length=8, validators=[RegexValidator(r'^\d{1,10}$', message='Debe ser 8 digitos', code='nomatch')], blank=False, null=False)
    phone_number = models.CharField('telefono/celular', max_length=15, blank=False, null=False)
    specialty = models.CharField('especialidad', max_length=100, blank=False, null=False)
    birthday = models.DateField('fecha de nacimiento', blank=False, null=False)
    reason_to_belong = models.TextField('motivo por el que quieren pertenecer a la red de emprendedores Jaku', blank=False, null=False)
    is_pending = models.BooleanField(default=True)
    temp_pwd = models.CharField(max_length=10, blank=True, null=True)
    country =  models.CharField('pais', max_length=100, blank=False, null=False)
    state =  models.CharField('estado', max_length=100, blank=True, null=True, default = '')
    city =  models.CharField('ciudad', max_length=100, blank=True, null=True, default = '')
    institution =  models.CharField('institucion', max_length=100, blank=False, null=False)
    career =  models.CharField('carrera', max_length=100, blank=True, null=True)
    year_income =  models.CharField('anho_ingreso', max_length=100, blank=True, null=True)
    sex = models.CharField('sexo', max_length=1, choices=SEX_CHOICES, null=False)

    def __str__(self):
        return f'{self.user.username} profile'

# Extension of user model for jury users
class ProfileJury(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField('telefono/celular', max_length=20, blank=False, null=False)

    def __str__(self):
        return self.user.username

# Extension of user model for mentor users
class ProfileMentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField('telefono/celular', max_length=20, blank=False, null=False)
    specialty = models.CharField('especialidad', max_length=150, blank=False, null=False)

    def __str__(self):
        return self.user.username

class ProfileCoach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField('telefono/celular', max_length=20, blank=False, null=False)

    def __str__(self):
        return self.user.username
        