from django.db import models
from django.core.validators import MinValueValidator

CATEGORIES_CHOICES = [("other", "Разное"), ("electronics", "Электроника"), ("books", "Книги"),
                      ("stationery", "Канцтовары")]


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Наименование товара')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание товара')
    category = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, default=CATEGORIES_CHOICES[0][0],
                                verbose_name="Категория")
    balance = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Стоимость",
                                validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.id}. {self.name} - {self.balance}'


class Cart(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='cart', verbose_name='Товар')
    qty = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} - {self.qty}'

    def get_product_total(self):
        return self.qty * self.product.price

    @classmethod
    def get_total(cls):
        total = 0
        for cart in cls.objects.all():
            total += cart.get_product_total()
        return total


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE, verbose_name='Заказ')
    qty = models.PositiveIntegerField(verbose_name='Количество')


class Order(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name='Телефон')
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    products = models.ManyToManyField('webapp.Product', related_name='order', through='webapp.OrderProduct',
                                      through_fields=['order', 'product'], verbose_name='Товары')
