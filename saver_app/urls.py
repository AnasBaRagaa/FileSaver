from django.urls import path

from saver_app import views

app_name = "saver_app"
urlpatterns = [
    path('', views.index,name='index'),
]
