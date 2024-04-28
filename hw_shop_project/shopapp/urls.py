from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_client/', views.create_client, name='create_client'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_client/<int:id>/', views.delete_client, name='delete_client'),

]
