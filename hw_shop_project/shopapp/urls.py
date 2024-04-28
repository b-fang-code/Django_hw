from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_client/', views.create_client, name='create_client'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_order/', views.create_order, name='create_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
]
