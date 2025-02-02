from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Watches(models.Model):
    title = models.CharField(max_length=155, verbose_name='Sarlavha')
    slug = models.SlugField(blank=True, unique=True)
    brand = models.CharField(max_length=155, verbose_name='Brand')
    description = models.TextField()
    quantity = models.IntegerField(default=0, verbose_name="Product Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(max_length=200,upload_to='images/%Y/%m/%d', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Watches, self).save(*args, **kwargs)

    def get_discount_price(self):
        if self.discount_percentage:
            discount_amount = self.price * (self.discount_percentage / 100)
            discounted_price = self.price - discount_amount
            return round(discounted_price, 2)  # Return as float with two decimal places
        return round(self.price, 2)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=155, verbose_name="Kategoriya")

    def __str__(self) -> str:
        return self.title


class News(models.Model):
    title = models.CharField(max_length=155, verbose_name='Sarlavha')
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqti')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    def __str__(self):
        return str(self.customer.name)  # Ensure customer name is converted to string

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderProduct(models.Model):
    product = models.ForeignKey(Watches, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        if self.product:
            price = self.product.get_discount_price() if self.product.discount_percentage else self.product.price
            total_price = price * self.quantity
            return total_price  # Ensure this returns a numeric value, not a formatted string

        return 0

    def __str__(self):
        return self.product.title if self.product else "No Product"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

