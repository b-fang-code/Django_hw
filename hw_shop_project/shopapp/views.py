from django.http import HttpResponse
from faker import Faker
from .models import Client, Product, Order, OrderItem
import random


def index(request):
    return HttpResponse("My shop")


fake = Faker()


def create_client(request):
    name = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    address = fake.address()
    client = Client(name=name, email=email, phone_number=phone_number, address=address)
    client.save()
    return client


def create_product(request):
    name = fake.text(max_nb_chars=100)
    description = fake.text()
    price = round(random.uniform(1, 1000), 2)
    quantity = random.randint(1, 100)
    product = Product(name=name, description=description, price=price, quantity=quantity)
    product.save()
    return product


def create_order(request, client, products):
    order = Order(client=client)
    order.save()
    for product in products:
        order_item = OrderItem(order=order, product=product)
        order_item.save()
    order.save()
    return order


def get_client(request, client_id):
    client = Client.objects.get(id=client_id)
    return client


def get_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return product


def get_order(request, order_id):
    order = Order.objects.get(id=order_id)
    return order


def delete_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return 'Client deleted'


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return 'Product deleted'


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return 'Order deleted'
