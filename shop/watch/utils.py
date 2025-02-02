from django.contrib import messages
#
from .models import Customer, Order, Watches, OrderProduct


class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={'name': self.user.username, 'email': self.user.email}
        )
        order, created = Order.objects.get_or_create(
            customer=customer,
            is_completed=False
        )

        order_products = order.orderproduct_set.all()
        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity
        

        return {
            "products": order_products,
            "order": order,
            "cart_total_price": cart_total_price,
            "cart_total_quantity": cart_total_quantity
        }

    def add_or_delete(self, product_id, action):
        cart_info = self.get_cart_info()
        order = cart_info["order"]
        product = Watches.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == "add" and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        elif action == "remove":
            order_product.quantity -= 1
            product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()


def get_cart_data(request):
    cart_info = {
        "products": [],
        "order": None,
        "cart_total_price": 0,
        "cart_total_quantity": 0
    }

    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

    return cart_info
