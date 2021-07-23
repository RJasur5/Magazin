from django.contrib.auth.signals import user_logged_in
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib.auth.models import Group

from .models import *
from .mixins import *
from .forms import *
from .utils import recalc_cart
    

class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, DetailView):

    context_object_name = 'product'
    template_name = 'product_detail.html'
    id_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):

    model = Category 
    queryset = Category.objects.all()
    category_products = Product.objects.filter(category=queryset)
    context_object_name = 'category'
    template_name = 'category_detail.html'
    name_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context 


# def CategoryDetail(request, pk):

#     category = Category.objects.get(id=pk)
#     product = Product.objects.filter(category=category)

#     return render(request, 'category.html', {'category': category, 'product': product})


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product = Product.objects.get(id=product_id)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product = Product.objects.get(id=product_id)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product = Product.objects.get(id=product_id)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        category = Category.objects.all()
        context = {'form': form, 'category': category, 'cart': self.cart}
        return render(request, 'login.html', context)


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {'form': form, 'cart': self.cart})


def RegisterPage(request):

        users = CreateUserForm()

        if request.method == 'POST':
            users = CreateUserForm(request.POST)
            if users.is_valid():
                user = users.save()
                users = Group.objects.get(name='users')
                user.groups.add(users)
                users.save()
                messages.success(request, "Account is created successfully")
                return redirect('login')
        return render(request, 'registration.html', {'users': users})


class OrderView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        category = Category.objects.all()
        return render(request, 'userorder.html', {'orders': orders, 'cart': self.cart, 'category': category,})

class ProfileView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.all()
        products = Product.objects.all()
        userorders = request.user.customer

        return render(request, 'profile.html', {'cart': self.cart, 'userorders': userorders, 'customer': customer,})


def ProfilSettings(request):

    user = request.user.customer
    p_form = CustomerForm(instance=user)

    if request.method == 'POST':
        p_form = CustomerForm(request.POST, request.FILES, instance=user)
        if p_form.is_valid():
            p_form.save()

    return render(request, 'profile_settings.html', {'p_form': p_form})

