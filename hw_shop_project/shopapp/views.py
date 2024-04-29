from django.shortcuts import get_object_or_404
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


def create_order(request, client_id, product_ids):
    client = get_object_or_404(Client, id=client_id)
    product_ids = product_ids.split(',')
    products = Product.objects.filter(id__in=product_ids)

    if products.count() != len(product_ids):
        return HttpResponse('One or more products do not exist')

    order = Order(client=client)
    order.save()

    for product in products:
        order.products.add(product)

    # Вызываем save() после добавления продуктов для обновления total_sum
    order.save()

    return HttpResponse(f'Order created for {client.name} with total sum {order.total_sum}')


def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return HttpResponse('Client deleted')


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponse('Product deleted')
