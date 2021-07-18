
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.ProductView.as_view(), name="index"),
    path('store/', views.store, name="store"),
    path('product_detail/<int:pk>',
         views.ProductDetailView.as_view(), name="product_detail"),
    path('contact/', views.contact, name="contact"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('blogs/', views.blogs, name='blogs'),
    path('about/', views.about, name='about'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('GeneratePdf/', views.GeneratePdf.as_view(), name='GeneratePdf'),



]
