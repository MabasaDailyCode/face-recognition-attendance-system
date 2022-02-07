from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home_view', views.home_view, name='home_view'),
    path('Menu', views.home, name='home'),
    path('register', views.register, name='register'),
    path('video', views.video_cap, name='video_cap'),
    path('Attendance', views.take_attendance, name='take_attendance'),
]