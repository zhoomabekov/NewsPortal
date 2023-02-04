from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)

class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.TextField()
    position = models.CharField(max_length=2, choices= POSITIONS, default= cashier)
    labor_contract = models.IntegerField()

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default= 0.0)
    pickup = models.IntegerField()
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through= "Product_Order")

class Product_Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

class Author(models.Model):
    full_name = models.CharField()
    age = models.IntegerField(blank=True)
    email = models.CharField(blank=True)