import datetime
import json
import num2words

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
from .models import Invoice
from .models import Product
from .models import Item
from .models import UserProfile
from .models import Inventory
from .models import InventoryLog


from .utils import invoice_data_dispdlts_validator, invoice_data_validator
from .utils import invoice_data_processor
from .utils import update_products_from_invoice
from .utils import update_items_from_invoice
from .utils import update_inventory
from .utils import create_inventory
from .utils import remove_inventory_entries_for_invoice

from .forms import DispdltsForm 
from .forms import ShipdltsForm
from .forms import ProductForm
from .forms import ItemForm
from .forms import UserProfileForm
from .forms import InventoryLogForm

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
        return redirect("invoice_create")
    context = {}
    auth_form = AuthenticationForm(request)
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            if user:
                login(request, user)
                return redirect("invoice_create")
        else:
            context["error_message"] = auth_form.get_invalid_login_error()
    context["auth_form"] = auth_form
    return render(request, 'login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("invoice_create")
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
            return redirect("invoice_create")



    return render(request, 'signup.html', context)



# Invoice, products===============================================

@login_required
def invoice_create(request):
    # if business info is blank redirect to update it
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if not user_profile.business_title:
        return redirect('user_profile_edit')

    context = {}
    context['default_invoice_number'] = Invoice.objects.filter(user=request.user).aggregate(Max('invoice_number'))['invoice_number__max']
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST

        validation_error = invoice_data_validator(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'invoice_create.html', context)

        # valid invoice data
        print("Valid Invoice Data")

        invoice_data_processed = invoice_data_processor(invoice_data)
        # save product
        update_products_from_invoice(invoice_data_processed, request)
        update_items_from_invoice(invoice_data_processed, request)

 # save invoice
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(user=request.user,
                              invoice_number=int(invoice_data['invoice-number']),
                              invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'),
                              invoice_data_dispdlts_validator = dispdltss, invoice_json=invoice_data_processed_json)
        new_invoice.save()
        print("INVOICE SAVED")

        update_inventory(new_invoice, request)
        print("INVENTORY UPDATED")



        return redirect('invoice_viewer', invoice_id=new_invoice.id)

    return render(request, 'invoice_create.html', context)


@login_required
def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'invoices.html', context)


@login_required
def invoice_viewer(request, invoice_id):
    invoice_obj = get_object_or_404(Invoice, user=request.user, id=invoice_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {}
    context['invoice'] = invoice_obj
    context['invoice_data'] = json.loads(invoice_obj.invoice_json)
    print(context['invoice_data'])
    context['currency'] = "₹"
    context['total_in_words'] = num2words.num2words(int(context['invoice_data']['invoice_total_amt_with_gst']), lang='en_IN').title()
    context['user_profile'] = user_profile
    return render(request, 'invoice_printer.html', context)


@login_required
def invoice_delete(request):
    if request.method == "POST":
        invoice_id = request.POST["invoice_id"]
        invoice_obj = get_object_or_404(Invoice, user=request.user, id=invoice_id)
        if len(request.POST.getlist('inventory-del')):
            remove_inventory_entries_for_invoice(invoice_obj, request.user)
        invoice_obj.delete()
    return redirect('invoices')



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
def shipdlts_edit(request, shipdlts_gstin):
    shipdlts_obj = get_object_or_404(Shipdlts, user=request.user, id=shipdlts_gstin)
    if request.method == "POST":
        shipdlts_form = ShipdltsForm(request.POST, instance=shipdlts_obj)
        if shipdlts_form.is_valid():
            new_shipdlts = shipdlts_form.save()
            return redirect('shipdltss')
    context = {}
    context['shipdlts_form'] = ShipdltsForm(instance=shipdlts_obj)
    return render(request, 'shipdlts_edit.html', context)

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
        shipdlts_gstin = request.POST["shipdlts_gstin"]
        shipdlts_obj = get_object_or_404(Shipdlts, user=request.user, id=shipdlts_gstin)
        shipdlts_obj.delete()
    return redirect('shipdltss')



@login_required
def dispdlts_add(request):
    if request.method == "POST":
        dispdlts_form = DispdltsForm(request.POST)
        new_dispdlts = dispdlts_form.save(commit=False)
        new_dispdlts.user = request.user
        new_dispdlts.save()
        # create dispdlts book
        # add_dispdlts_book(new_dispdlts)
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
        # create shipdlts book
        # add_shipdlts_book(new_shipdlts)
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
            create_inventory(new_product)

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
            create_inventory(new_item)

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



# ================= Inventory Views ===========================
@login_required
def inventory(request):
    context = {}
    context['inventory_list'] = Inventory.objects.filter(user=request.user)
    context['untracked_products'] = Product.objects.filter(user=request.user, inventory=None)
    return render(request, 'inventory.html', context)

@login_required
def inventory(request):
    context = {}
    context['inventory_list'] = Inventory.objects.filter(user=request.user)
    context['untracked_items'] = Item.objects.filter(user=request.user, inventory=None)
    return render(request, 'inventory.html', context)

@login_required
def inventory_logs(request, inventory_id):
    context = {}
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    inventory_logs = InventoryLog.objects.filter(user=request.user, product=inventory.product).order_by('-id')
    context['inventory'] = inventory
    context['inventory_logs'] = inventory_logs
    return render(request, 'inventory_logs.html', context)

@login_required
def inventory_logs(request, inventory_id):
    context = {}
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    inventory_logs = InventoryLog.objects.filter(user=request.user, item=inventory.item).order_by('-id')
    context['inventory'] = inventory
    context['inventory_logs'] = inventory_logs
    return render(request, 'inventory_logs.html', context)

@login_required
def inventory_logs_add(request, inventory_id):
    context = {}
    inventory = get_object_or_404(Inventory, id=inventory_id, user=request.user)
    inventory_logs = Inventory.objects.filter(user=request.user, product=inventory.product)
    inventory_logs = Inventory.objects,filter(user=request.user, item=inventory.item)
    context['inventory'] = inventory
    context['inventory_logs'] = inventory_logs
    context['form'] = InventoryLogForm()

    if request.method == "POST":
        inventory_log_form = InventoryLogForm(request.POST)
        invoice_no = request.POST["invoice_no"]
        invoice = None
        if invoice_no:
            try:
                invoice_no = int(invoice_no)
                invoice = Invoice.objects.get(user=request.user, invoice_number=invoice_no)
            except:
                context['error_message'] = "Incorrect invoice number %s"%(invoice_no,)
                return render(request, 'inventory_logs_add.html', context)
                context['form'] = inventory_log_form
                return render(request, 'inventory_logs_add.html', context)


        inventory_log = inventory_log_form.save(commit=False)
        inventory_log.user = request.user
        inventory_log.product = inventory.product
        inventory_log.item  = inventory.item
        if invoice:
            inventory_log.associated_invoice = invoice
        inventory_log.save()
        inventory.current_stock = inventory.current_stock + inventory_log.change
        inventory.last_log = inventory_log
        inventory.save()
        return redirect('inventory_logs', inventory.id)

    
    return render(request, 'inventory_logs_add.html', context)

# ================= Static Pages ==============================

def landing_page(request):
    context = {}
    return render(request, 'landing_page.html', context)
