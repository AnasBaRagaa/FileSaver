from django.urls import path

from saver_app import views

app_name = "saver_app"
urlpatterns = [
    path('', views.IndexClass.as_view(), name='index'),
    path('add', views.CreateData.as_view(), name='add'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path("share/<int:pk>/", views.create_sharing_link, name='share'),
    path("details/<int:pk>/", views.DetailView.as_view(), name='details'),
    path("public/<int:pk>/", views.public_link, name='public'),
    path("deletelink/<int:pk>/", views.DeleteLinkView.as_view(), name='deleteLink')
]
