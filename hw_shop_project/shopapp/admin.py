from django.contrib import admin
from .models import Product, Client, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    list_filter = ('name', 'price', 'quantity')
    search_fields = ('name', 'price', 'quantity')
    readonly_fields = ('date',)
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Подробное описание товара',
                'fields': ['description'],
            },
        ),
        (
            'Бухгалтерия',
            {
                'fields': ['price', 'quantity'],
            }
        ),
        (
            'Прочее',
            {
                'fields': ['date'],
            }
        ),
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address')
    list_filter = ('name', 'phone', 'email', 'address')
    search_fields = ('name', 'phone', 'email', 'address')
    readonly_fields = ('date',)
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            }
        ),
        (
            'Информация',
            {
                'classes': ['collapse'],
                'description': 'Информация о клиенте',
                'fields': ['phone', 'email', 'address'],
            }
        ),
        (
            'Прочее',
            {
                'fields': ['date'],
            }
        )
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'total_sum', 'date')
    list_filter = ('client', 'total_sum', 'date')
    search_fields = ('client', 'total_sum', 'date')
    readonly_fields = ('date',)
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['client'],
            }
        ),
        (
            'Информация',
            {
                'classes': ['collapse'],
                'description': 'Информация о заказе',
                'fields': ['total_sum'],
            }
        ),
        (
            'Прочее',
            {
                'fields': ['date'],
            }
        )
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
