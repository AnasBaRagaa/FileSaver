from django.urls import path

from saver_app import views

app_name = "saver_app"
urlpatterns = [
    path('', views.IndexClass.as_view(),name='index'),
    path('add',views.CreateData.as_view(),name='add')
]
