from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.core.files.storage import FileSystemStorage
from .models import Client, Product, Order
from .forms import ChoiceForm, ClientForm, ProductForm, DeleteByIdForm
import datetime


def main(request):
    return render(request, 'shopapp/base.html')


def orders_by_period(request):
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
    return render(request, 'shopapp/orders_by_period.html', {'form': form})


def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        message = 'Ошибка данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
            client = Client(name=name, email=email, phone=phone, address=address, date=date)
            client.save()
            message = 'Клиент создан'
            return redirect('main')
    else:
        form = ClientForm()
        message = 'Заполните форму'
    return render(request, 'shopapp/create_client.html', {'form': form, 'message': message})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        message = 'Ошибка данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
            product = Product(name=name, price=price, description=description, quantity=quantity, image=image)
            product.save()
            return redirect('main')
    else:
        form = ProductForm()
        message = 'Заполните форму'
    return render(request, 'shopapp/create_product.html', {'form': form, 'message': message})


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


def delete_product(request):
    if request.method == 'POST':
        form = DeleteByIdForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['id']
            if product_id not in [product.id for product in Product.objects.all()]:
                return HttpResponse('Продукта с таким id не существует в базе данных' + '<br>' + '<a href="">Назад</a>')
            product = Product.objects.get(id=product_id)
            product.delete()
            return redirect('get_all_products')
    else:
        form = DeleteByIdForm()
    return render(request, 'shopapp/delete_product.html', {'form': form})


def delete_client(request):
    if request.method == 'POST':
        form = DeleteByIdForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data['id']
            if client_id not in [client.id for client in Client.objects.all()]:
                return HttpResponse('Клиента с таким id не существует в базе данных' + '<br>' + '<a href="">Назад</a>')
            client = Client.objects.get(id=client_id)
            client.delete()
            return redirect('get_all_clients')
    else:
        form = DeleteByIdForm()
    return render(request, 'shopapp/delete_client.html', {'form': form})


def delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return HttpResponse('Order deleted')


def orders_by_week(request, client_id):
    if client_id not in [client.id for client in Client.objects.all()]:
        return HttpResponse('Клиента с таким id не существует в базе данных' + '<a href="">Назад</a>')
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=7))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за неделю', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)


def orders_by_month(request, client_id):
    if client_id not in [client.id for client in Client.objects.all()]:
        return HttpResponse('Клиента с таким id не существует в базе данных' + '<a href="">Назад</a>')
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=30))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за месяц', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)


def orders_by_year(request, client_id):
    if client_id not in [client.id for client in Client.objects.all()]:
        return HttpResponse('Клиента с таким id не существует в базе данных' + '<a href="">Назад</a>')
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client, date__gte=datetime.datetime.now() - datetime.timedelta(days=365))
    products = Product.objects.filter(orders__in=orders).distinct().order_by('-orders__date')

    prefetch_related_orders = Prefetch('orders', orders)
    products = products.prefetch_related(prefetch_related_orders)

    context = {'title': 'Заказы за год', 'client': client.name, 'products': products}
    return render(request, 'shopapp/orders_by.html', context)


def get_all_clients(request):
    clients = Client.objects.all()
    context = {'title': 'Все клиенты', 'clients': clients}
    return render(request, 'shopapp/all_clients.html', context)


def get_all_products(request):
    products = Product.objects.all()
    context = {'title': 'Все продукты', 'products': products}
    return render(request, 'shopapp/all_products.html', context)
