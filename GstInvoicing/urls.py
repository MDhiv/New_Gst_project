from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('products/add', views.product_add, name='product_add'),

    path('login', views.login_view, name='login_view'),
    path('signup', views.signup_view, name='signup_view'),
    path('accounts/', include('django.contrib.auth.urls')),

    
    path('dispdltss', views.dispdltss, name='dispdltss'),
    path('dispdlts/<int:dispdlts_id>', views.dispdlts_viewer, name='dispdlts_viewer'),
    path('dispdltss/add', views.dispdlts_add, name='dispdlts_add'),
    path('dispdltss/edit/<int:dispdlts_id>', views.dispdlts_edit, name='dispdlts_edit'),
    path('dispdltss/delete', views.dispdlts_delete, name='dispdlts_delete'),
    path('displtssjson', views.dispdltssjson, name='dispdltssjson'),

    path('shipdltss', views.shipdltss, name='shipdltss'),
    path('shipdlts/<int:shipdlts_id>', views.shipdlts_viewer, name='shipdlts_viewer'),
    path('shipltss/add', views.shipdlts_add, name='shipdlts_add'),
    path('shipdltss/edit/<int:shipdlts_id>', views.shipdlts_edit, name='shipdlts_edit'),
    path('shipdltss/delete', views.shipdlts_delete, name='shipdlts_delete'),
    path('shipdltssjson', views.shipdltssjson, name='shipdltssjson'),

    path('products', views.products, name='products'),
    path('products/add', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>', views.product_edit, name='product_edit'),
    path('products/delete', views.product_delete, name='product_delete'),
    path('productsjson', views.productsjson, name='productsjson'),

    path('items', views.items, name='items'),
    path('items/add', views.item_add, name='item_add'),
    path('items/edit/<int:item_id>', views.item_edit, name='item_edit'),
    path('items/delete', views.item_delete, name='item_delete'),
    path('itemsjson', views.itemsjson, name='itemsjson'),

    path('profile', views.user_profile, name='user_profile'),
    path('profile/edit', views.user_profile_edit, name='user_profile_edit'),


] 