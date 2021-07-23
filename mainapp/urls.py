from django.urls import path

from .views import *
from . import views


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    # path('<str:pk>/', views.CategoryDetail, name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:id>/', ChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('userorder/', OrderView.as_view(), name='userorder'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profilesettings/', views.ProfilSettings, name='profilesettings'),


    path('login/', LoginView.as_view(), name='login'),
    path('registration/', views.RegisterPage, name='registration'),

]
