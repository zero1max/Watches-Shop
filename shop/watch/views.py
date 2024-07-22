from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, FurnitureModelForm, ShippingAddressForm, CustomerForm
from .models import Watches, Category, News, Customer, Order
from .serializers import WatchesSerializer
import random
from .utils import get_cart_data, CartForAuthenticatedUser
from django.conf import settings
from django.utils.text import slugify
from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

import stripe

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'watch/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Signup'
        return context
    
class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'watch/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
    
def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    watches = list(Watches.objects.filter(is_published=True))
    random.shuffle(watches)
    categories = Category.objects.all()
    news = News.objects.filter(is_published=True)
    context = {
        'watches': watches,
        'categories': categories,
        'news': news,
        'title': 'Home',
    }
    return render(request, 'watch/home.html', context)

def shop(request):
    furnitures = Watches.objects.filter(is_published=True)
    categories = Category.objects.all()
    random_watches = list(Watches.objects.filter(is_published=True))
    random.shuffle(random_watches)

    # Paginatorni yaratish
    paginator = Paginator(furnitures, 6)  # Har bir sahifada 10 ta mebel ko'rsatiladi
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'random_watches': random_watches,
        'page_obj': page_obj,
        'categories': categories,
        'title': 'Shop'
    }
    return render(request, 'watch/shop.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = Watches.objects.filter(title__icontains=query, is_published=True) if query else []
    context = {
        'query': query,
        'results': results,
        'title':'Search'
    }
    return render(request, 'watch/search.html', context)

class WatchesView(ListAPIView):
    queryset = Watches.objects.all()
    serializer_class = WatchesSerializer

class WatchesViewCRUD(RetrieveUpdateDestroyAPIView):
    queryset = Watches.objects.all()
    serializer_class = WatchesSerializer

class WatchesDetailView(DetailView):
    model = Watches
    template_name = 'watch/watch_detail.html'
    context_object_name = 'watch'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Watches, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Watch Detail'
        return context

class CategoryView(DetailView):
    model = Category
    template_name = 'watch/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watches'] = Watches.objects.filter(category_id=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        return context
    
class NewsView(ListView):
    model = News
    template_name = 'watch/news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News'
        return context
    
class NewsDetailView(DetailView):
    model = News
    template_name = 'watch/news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(News, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News Detail'
        return context
    
def cart(request):
    cart_info = get_cart_data(request)
    context = {
        "products": cart_info["products"],
        "order": cart_info["order"],
        "cart_total_price": cart_info["cart_total_price"],
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "title": "Cart"
    }
    return render(request, 'watch/cart.html', context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        messages.error(request, "You are not authenticated")
        return redirect('login')
    
def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products'],
        'customer_form': CustomerForm,
        'shipping_form': ShippingAddressForm,
        'title': "checkout"
    }
    return render(request, 'watch/checkout.html', context)

def clear_cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer=customer, is_completed=False).first()
        if order:
            order.orderproduct_set.all().delete()  # Clear all order products
        messages.success(request, "Your cart has been cleared.")
    else:
        messages.error(request, "You need to be logged in to clear the cart.")
    return redirect('cart')

def payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.name = customer_form.cleaned_data['name']
            customer.email = customer_form.cleaned_data['email']
        shipping_form = ShippingAddressForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': "Products of IboCo"
                        },
                        'unit_amount': int(total_price)
                    },
                    'quantity': total_quantity
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('success'))
        )
        return redirect(session.url, 303)

def payment_success(request):
    return render(request,"watch/success.html")

