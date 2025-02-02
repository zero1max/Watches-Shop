from django.urls import path
#
from .views import RegisterView, CustomLoginView, user_logout, home,\
    shop, search, WatchesView, WatchesViewCRUD, WatchesDetailView, CategoryView,\
    NewsView, NewsDetailView, cart, to_cart, checkout, payment, payment_success, clear_cart

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('watch/<slug:slug>/', WatchesDetailView.as_view(), name='detail_url'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category_url'),
    path('shop/', shop, name='shop'),
    path('search/', search, name='search'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail_url'),
    path('logout/', user_logout, name='logout'),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("to_cart/<int:product_id>/<str:action>/", to_cart, name="to_cart"),
    path("payment/", payment, name="payment"),
    path("success/", payment_success, name="success"),
    path("watches/", WatchesView.as_view(), name="watches"),
    path('watches/<int:pk>/', WatchesViewCRUD.as_view(), name="watchesCRUD"),
    path('clear_cart/', clear_cart, name='clear_cart'),
]
