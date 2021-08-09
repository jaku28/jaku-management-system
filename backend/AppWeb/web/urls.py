from django.urls import path
from . import views
from . import models

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('historia',views.history, name ='history'),
    path('organigrama',views.organizationchart, name='organizationchart'),
    path('mision-vision', views.missionvision, name='missionvision'),
    path('directorio-mentores', views.directorymentors, name='directorymentors'),
    path('emprendimientos',views.ventures, name = 'ventures'),
    path('convocatorias',views.calls, name = 'calls'),
    path('noticias',views.news, name = 'news'),
    path('eventos',views.events, name = 'events'),
    path('contactenos',views.contact, name = 'contact'),
    path('evento/<int:event_id>/', views.event_detail, name='eventdetail'),
    path('noticia/<int:new_id>/', views.new_detail, name='newdetail'),
    path('convocatoria/<int:call_id>/',views.call_detail, name='calldetail'),
]