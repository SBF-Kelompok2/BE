from django.urls import path
from main.views import show_main, show_xml, show_json, show_json_by_id, register, login_user, logout_user, edit_product, delete_product #edit_mood, delete_mood ,create_mood_entry
from main.views import show_main, create_product_entry, my_product
from . import views
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-product/', my_product, name='my-product'),


    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('delete/<uuid:id>', delete_product, name='delete_product'), # sesuaikan dengan nama fungsi yang dibuat
    path('create-product-entry', create_product_entry, name='create_product_entry'),

    path('cart/', views.show_cart, name='show_cart'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]