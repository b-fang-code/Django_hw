from django.db.models import Sum
from django.http import HttpResponse
from .models import Client, Product, Order
from faker import Faker
import datetime


def index(request):
    return HttpResponse("MyShop")


def create_client(request):
    client = Client.objects.create(
        name=Faker().name(), email=Faker().email(), phone=Faker().phone_number(), address=Faker().address(),
        date=datetime.datetime.now()
    )
    client.save()
    return HttpResponse('Client created')


def create_product(request):
    product = Product.objects.create(
        name=Faker().company(), description=Faker().text(), price=Faker().pyint(), quantity=Faker().pyint(),
        date=datetime.datetime.now()
    )
    product.save()
    return HttpResponse('Product created')


def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return HttpResponse('Client deleted')


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponse('Product deleted')
