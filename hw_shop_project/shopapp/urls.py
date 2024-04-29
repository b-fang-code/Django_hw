from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_client/', views.create_client, name='create_client'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_client/<int:id>/', views.delete_client, name='delete_client'),
    path('create_order/<int:client_id>/<str:product_ids>/', views.create_order, name='create_order'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),
]
