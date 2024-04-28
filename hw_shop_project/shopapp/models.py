from django.db import models


# Создайте три модели Django: клиент, товар и заказ.
# Клиент может иметь несколько заказов. Заказ может содержать несколько товаров. Товар может входить в несколько заказов.
# Поля модели «Клиент»:
# — имя клиента
# — электронная почта клиента
# — номер телефона клиента
# — адрес клиента
# — дата регистрации клиента
# Поля модели «Товар»:
# — название товара
# — описание товара
# — цена товара
# — количество товара
# — дата добавления товара
# Поля модели «Заказ»:
# — связь с моделью «Клиент», указывает на клиента, сделавшего заказ
# — связь с моделью «Товар», указывает на товары, входящие в заказ
# — общая сумма заказа
# — дата оформления заказа
# Допишите несколько функций CRUD для работы с моделями ОБЯЗАТЕЛЬНО(create_client, create_product, create_order).
# Используй библиотеку fake для создания новых клиентов и продуктов. Еще мне нужно, чтобы в таблице order считалась
# общая сумма заказа. Html здесь мы не используем. Просто создаем таблицы
# в базе данных.Еще допиши представления get_client, get_prouduct и get_order, delete_client, delete_product, delete_order


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    total_sum = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.client)


