from django.shortcuts import render, redirect, reverse   # Tambahkan import redirect di baris ini
from main.forms import ProductEntryForm #MoodEntryForm,
from main.models import ProductEntry #MoodEntry,
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

import datetime
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/login')
# def show_main(request):

#     mood_entries = MoodEntry.objects.filter(user=request.user)

#     context = {
#         'name': request.user.username,
#         'class': 'PBP D',
#         'npm': '2306123456',
#         'mood_entries': mood_entries,
#         'last_login': request.COOKIES['last_login'],
#     }

#     return render(request, "main.html", context)

def show_main(request):

    product_entries = ProductEntry.objects.filter(user=request.user)

    context = {
        'name': request.user.username, #nama user
        'product_entries': product_entries,

        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)


# def create_mood_entry(request):
#     form = MoodEntryForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         mood_entry = form.save(commit=False)
#         mood_entry.user = request.user
#         mood_entry.save()
#         return redirect('main:show_main')

#     context = {'form': form}
#     return render(request, "create_mood_entry.html", context)

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
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
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