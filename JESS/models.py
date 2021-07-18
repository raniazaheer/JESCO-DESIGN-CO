from django.db import models

# Create your models here.
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.query import BaseIterable
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

category_choices = (
    ('F', 'Frames'),
    ('P', 'oil_paintings'),
    ('S', 'sketching'),
    ('D', 'drawing'),
)


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    product_image1 = models.ImageField(upload_to='images')
    product_date = models.DateTimeField(auto_now=True)
    desc = models.TextField()
    discount_price = models.FloatField()
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=category_choices, max_length=5)

    def __str__(self):
        return self.product_name


class users(models.Model):
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)

    # additional fields
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('DElivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField()
    transaction_id = models.CharField(max_length=250, null=True)
    delivery = models.DecimalField(max_digits=7, decimal_places=2, default=150)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_tot_del(self):
        total = (self.get_cart_total) + 150
        return total

    @property
    def shipping(self):
        shipping = True
        return shipping


class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name + "-" + self.email


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id)

    @property
    def get_total(self):
        total = (self.product.product_price) * (self.quantity)
        return total


class ShippingAdddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
