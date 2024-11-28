from django.shortcuts import render, redirect, reverse, get_object_or_404
from main.forms import ProductEntryForm, CustomUserCreationForm, UserEditForm
from main.models import ProductEntry, UserData, ProductEntry, Cart, CartItem
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserDataSerializer

@login_required(login_url='/login')
def show_main(request):

    product_entries = ProductEntry.objects.filter(user=request.user)
    
    # Fetch the additional user data (e.g., address)
    user_data = None
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = None  # Handle case where no address exists

    context = {
        'name': request.user.username, #nama user
        'email': request.user.email,  # Email
        'address': user_data.address if user_data else "Address not available",
        'product_entries': product_entries,

        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

@login_required
def profile(request):
    # Fetch the additional user data (e.g., address)
    # user_data = None
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        user_data = UserData.objects.create(user=request.user, address="")  # Handle case where no address exists

    if request.method == 'POST':
        # Process profile update
        user_form = UserEditForm(request.POST, instance=request.user)
        address = request.POST.get('address')

        if user_form.is_valid():
            user_form.save()
            user_data.address = address
            user_data.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('main:profile')
        else:
            messages.error(request, "Error updating your profile. Please check the details.")
    else:
        # Pre-fill the form
        user_form = UserEditForm(instance=request.user)

    context = {
        'form': user_form,
        'address': user_data.address,
        'last_login': request.COOKIES.get('last_login', 'Unknown'),
    }
    return render(request, 'profile.html', context)

@login_required
def my_product(request):
    # Fetch products created by the logged-in user
    product_entries = ProductEntry.objects.filter(user=request.user)

    context = {
        'product_entries': product_entries,
    }
    return render(request, 'my_product.html', context)

def create_product_entry(request):
    form = ProductEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product_entry.html", context)

def show_xml(request):
    data = ProductEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data_product = ProductEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data_product), content_type="application/json")

def show_json_by_id(request, id):
    data_product = ProductEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data_product), content_type="application/json")

def register(request):
    form = CustomUserCreationForm()  # Instantiate the form

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        else:
            messages.error(request, "There was an error with your registration form.")
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")
          
   form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    # Get product entry berdasarkan id
    product = ProductEntry.objects.get(pk = id)

    # Set product entry sebagai instance dari form
    form = ProductEntryForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    # Get product berdasarkan id
    product = ProductEntry.objects.get(pk = id)
    # Hapus product
    product.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))


@login_required
def show_cart(request):
    # Fetch or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        "cart": cart,
        "cart_items": cart.items.all(),
        "total_price": sum(item.get_total_price() for item in cart.items.all()),
    }
    return render(request, "cart.html", context)

@login_required
def add_to_cart(request, product_id):
    product = ProductEntry.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("main:show_cart")

@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("main:show_cart")
