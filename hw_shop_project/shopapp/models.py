from django.db import models


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

    def save(self, *args, **kwargs):
        # Вычисляем общую сумму заказа только при обновлении существующего заказа
        if self.pk:
            self.total_sum = self.products.aggregate(total=models.Sum('price'))['total'] or 0
        super().save(*args, **kwargs)
