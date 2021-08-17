from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Max

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Dispdlts
from .models import Shipdlts
from .models import Product
from .models import Item
from .models import UserProfile


from .forms import DispdltsForm 
from .forms import ShipdltsForm
from .forms import ProductForm
from .forms import ItemForm
from .forms import UserProfileForm

# Create your views here.


# User Management =====================================

@login_required
def user_profile_edit(request):
    context = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context['user_profile_form'] = UserProfileForm(instance=user_profile)
    
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_profile_form.save()
        return redirect('user_profile')
    return render(request, 'user_profile_edit.html', context)


@login_required
def user_profile(request):
    context = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context['user_profile'] = user_profile
    return render(request, 'user_profile.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("product_add")
    context = {}
    auth_form = AuthenticationForm(request)
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            if user:
                login(request, user)
                return redirect("product_add")
        else:
            context["error_message"] = auth_form.get_invalid_login_error()
    context["auth_form"] = auth_form
    return render(request, 'login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("product_add")
    context = {}
    signup_form = UserCreationForm()
    profile_edit_form = UserProfileForm()
    context["signup_form"] = signup_form
    context["profile_edit_form"] = profile_edit_form

    
    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        profile_edit_form = UserProfileForm(request.POST)
        context["signup_form"] = signup_form
        context["profile_edit_form"] = profile_edit_form

        if signup_form.is_valid():
            user = signup_form.save()
        else:
            context["error_message"] = signup_form.errors
            return render(request, 'signup.html', context)
        if profile_edit_form.is_valid():
            userprofile = profile_edit_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("product_add")
    return render(request, 'signup.html', context)



@login_required
def dispdltss(request):
    context = {}
    context['dispdltss'] = Dispdlts.objects.filter(user=request.user)
    return render(request, 'dispdltss.html', context)

@login_required
def shipdltss(request):
    context = {}
    context['shipdltss'] = Shipdlts.objects.filter(user=request.user)
    return render(request, 'shipdltss.html', context)

@login_required
def products(request):
    context = {}
    context['products'] = Product.objects.filter(user=request.user)
    return render(request, 'products.html', context)

@login_required
def items(request):
    context = {}
    context['items'] = Item.objects.filter(user=request.user)
    return render(request, 'items.html', context)

@login_required
def dispdltssjson(request):
    dispdltss = list(Dispdlts.objects.filter(user=request.user).values())
    return JsonResponse(dispdltss, safe=False)

@login_required
def shipdltssjson(request):
    shipdltss = list(Shipdlts.objects.filter(user=request.user).values())
    return JsonResponse(shipdltss, safe=False)

@login_required
def productsjson(request):
    products = list(Product.objects.filter(user=request.user).values())
    return JsonResponse(products, safe=False)

@login_required
def itemsjson(request):
    items = list(Item.objects.filter(user=request.user).values())
    return JsonResponse(items, safe=False)


@login_required
def dispdlts_edit(request, dispdlts_id):
    dispdlts_obj = get_object_or_404(Dispdlts, user=request.user, id=dispdlts_id)
    if request.method == "POST":
        dispdlts_form = DispdltsForm(request.POST, instance=dispdlts_obj)
        if dispdlts_form.is_valid():
            new_dispdlts = dispdlts_form.save()
            return redirect('dispdltss')
    context = {}
    context['dispdlts_form'] = DispdltsForm(instance=dispdlts_obj)
    return render(request, 'dispdlts_edit.html', context)

@login_required
def dispdlts_viewer(request, dispdlts_id):
    dispdlts_obj = get_object_or_404(Dispdlts, user=request.user, id=dispdlts_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {}
    context['dispdlts'] = dispdlts_obj
    context['user_profile'] = user_profile
    return render(request, 'dispdlts_printer.html', context)

@login_required
def shipdlts_edit(request, shipdlts_id):
    shipdlts_obj = get_object_or_404(Shipdlts, user=request.user, id=shipdlts_id)
    if request.method == "POST":
        shipdlts_form = ShipdltsForm(request.POST, instance=shipdlts_obj)
        if shipdlts_form.is_valid():
            new_shipdlts = shipdlts_form.save()
            return redirect('shipdltss')
    context = {}
    context['shipdlts_form'] = ShipdltsForm(instance=shipdlts_obj)
    return render(request, 'shipdlts_edit.html', context)

@login_required
def shipdlts_viewer(request, shipdlts_id):
    shipdlts_obj = get_object_or_404(Shipdlts, user=request.user, id=shipdlts_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {}
    context['shipdlts'] = shipdlts_obj
    context['user_profile'] = user_profile
    return render(request, 'shipdlts_printer.html', context)

@login_required
def dispdlts_delete(request):
    if request.method == "POST":
        dispdlts_id = request.POST["dispdlts_id"]
        dispdlts_obj = get_object_or_404(Dispdlts, user=request.user, id=dispdlts_id)
        dispdlts_obj.delete()
    return redirect('dispdltss')

@login_required
def shipdlts_delete(request):
    if request.method == "POST":
        shipdlts_id = request.POST["shipdlts_id"]
        shipdlts_obj = get_object_or_404(Shipdlts, user=request.user, id=shipdlts_id)
        shipdlts_obj.delete()
    return redirect('shipdltss')



@login_required
def dispdlts_add(request):
    if request.method == "POST":
        dispdlts_form = DispdltsForm(request.POST)
        new_dispdlts = dispdlts_form.save(commit=False)
        new_dispdlts.user = request.user
        new_dispdlts.save()
        return redirect('dispdltss')
    context = {}
    context['dispdlts_form'] = DispdltsForm()
    return render(request, 'dispdlts_edit.html', context)

@login_required
def shipdlts_add(request):
    if request.method == "POST":
        shipdlts_form = ShipdltsForm(request.POST)
        new_shipdlts = shipdlts_form.save(commit=False)
        new_shipdlts.user = request.user
        new_shipdlts.save()

        return redirect('shipdltss')
    context = {}
    context['shipdlts_form'] = ShipdltsForm()
    return render(request, 'shipdlts_edit.html', context)

@login_required
def product_edit(request, product_id):
    product_obj = get_object_or_404(Product, user=request.user, id=product_id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product_obj)
        if product_form.is_valid():
            new_product = product_form.save()
            return redirect('products')
    context = {}
    context['product_form'] = ProductForm(instance=product_obj)
    return render(request, 'product_edit.html', context)

@login_required
def item_edit(request, item_id):
    item_obj = get_object_or_404(Item, user=request.user, id=item_id)
    if request.method == "POST":
        item_form = ItemForm(request.POST, instance=item_obj)
        if item_form.is_valid():
            new_item = item_form.save()
            return redirect('items')
    context = {}
    context['item_form'] = ItemForm(instance=item_obj)
    return render(request, 'item_edit.html', context)

@login_required
def product_add(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.user = request.user
            new_product.save()

            return redirect('products')
    context = {}
    context['product_form'] = ProductForm()
    return render(request, 'product_edit.html', context)


@login_required
def product_delete(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        product_obj = get_object_or_404(Product, user=request.user, id=product_id)
        product_obj.delete()
    return redirect('products')

@login_required
def item_add(request):
    if request.method == "POST":
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            new_item = item_form.save(commit=False)
            new_item.user = request.user
            new_item.save()

            return redirect('items')
    context = {}
    context['item_form'] = ItemForm()
    return render(request, 'item_edit.html', context)


@login_required
def item_delete(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        item_obj = get_object_or_404(Item, user=request.user, id=item_id)
        item_obj.delete()
    return redirect('items')

# ================= Static Pages ==============================

def landing_page(request):
    context = {}
    return render(request, 'landing_page.html', context)
