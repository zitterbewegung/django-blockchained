from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate_pi', views.calculate_pi, name='calculate_pi')
    #path('<int:qblock_id>/', views.detail, name='detail'),
]
