from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Prefetch
from .models import Client, Product, Order
from .forms import ChoiceForm
from faker import Faker
import datetime


def index(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice_period']
            client_id = form.cleaned_data['client_id']
            if choice == 'week':
                return orders_by_week(request, client_id)
            if choice == 'month':
                return orders_by_month(request, client_id)
            if choice == 'year':
                return orders_by_year(request, client_id)
    else:
        form = ChoiceForm()
    return render(request, 'shopapp/index.html', {'form': form})


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


def delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return HttpResponse('Order deleted')


def orders_by_week(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=7))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за неделю', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)


def orders_by_month(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=30))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за месяц', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)


def orders_by_year(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=365))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за год', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)
