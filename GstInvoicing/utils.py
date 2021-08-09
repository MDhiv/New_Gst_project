import datetime
import json

from django.db.models import Sum


from .models import Product
from .models import Item 
from .models import Inventory
from .models import InventoryLog



def invoice_data_validator(invoice_data):

    try:
        invoice_number = int(invoice_data['invoice-number'])
    except:
        print("Error: Incorrect Invoice Number")
        return "Error: Incorrect Invoice Number"

    try:
        date_text = invoice_data['invoice-date']
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return "Error: Incorrect Invoice Date"




def invoice_data_dispdlts_validator(invoice_data):
    
    try:
        invoice_number = int(invoice_data['invoice-number'])
    except:
        print("Error: Incorrect Invoice Number")
        return "Error: Incorrect Invoice Number"

    try:
        date_text = invoice_data['invoice-date']
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return "Error: Incorrect Invoice Date"

    if len(invoice_data['dispdlts-name']) < 1 or len(invoice_data['dispdlts-name']) > 200:
        print("Error: Incorrect Dispdlts Name")
        return "Error: Incorrect Dispdlts Name"

    if len(invoice_data['dispdlts-address1']) > 300:
        print("Error: Incorrect Dispdlts Address1")
        return "Error: Incorrect Dispdlts Address1"

    if len(invoice_data['dispdlts-address2']) > 300:
        print("Error: Incorrect Dispdlts Address2")
        return "Error: Incorrect Dispdlts Address2"

    if len(invoice_data['dispdlts-loc']) > 15:
        print("Error: Incorrect Dispdlts Loc")
        return "Error: Incorrect Dispdlts Loc"

    if len(invoice_data['dispdlts-pin']) > 15:
        print("Error: Incorrect Dispdlts Pin")
        return "Error: Incorrect Dispdlts Pin"

    if len(invoice_data['dispdlts-stcd']) > 15:
        print("Error: Incorrect Dispdlts Stcd")
        return "Error: Incorrect Dispdlts Stcd"
    return None

def invoice_data_validator(invoice_data):

    try:
        invoice_number = int(invoice_data['invoice-number'])
    except:
        print("Error: Incorrect Invoice Number")
        return "Error: Incorrect Invoice Number"


    try:
        date_text = invoice_data['invoice-date']
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return "Error: Incorrect Invoice Date"


    if len(invoice_data['shipdlts-gstin']) > 20:
        print("Error: Incorrect Shipdlts Gstin")
        return "Error: Incorrect Shipdlts Gstin"

    if len(invoice_data['shipdlts-lglnm']) > 20:
        print("Error: Incorrect Shipdlts LglNm")
        return "Error: Incorrect Shipdlts LglNm"

    if len(invoice_data['shipdlts-trdnm']) > 20:
        print("Error: Incorrect Shipdlts LglNm")
        return "Error: Incorrect Shipdlts Lglnm"

    if len(invoice_data['shipdlts-addr1']) > 300:
        print("Error: Incorrect Shipdlts Addr1")
        return "Error: Incorrect Shipdlts Addr1"

    if len(invoice_data['shipdlts-addr2']) > 300:
        print("Error: Incorrect Shipdlts Addr2")
        return "Error: Incorrect Shipdlts Addr2"

    if len(invoice_data['shipdlts-loc']) > 20:
        print("Error: Incorrect Shipdlts Loc")
        return "Error: Incorrect Shipdlts Loc"

    if len(invoice_data['shipdlts-pin']) > 20:
        print("Error: Incorrect Shipdlts Pin")
        return "Error: Incorrect Shipdlts Pin"

    if len(invoice_data['shipdlts-stcd']) > 20:
        print("Error: Incorrect Shipdlts Stcd")
        return "Error: Incorrect Shipdlts Stcd"

    return None

def invoice_data_processor(invoice_post_data):
    print(invoice_post_data)
    processed_invoice_data = {}

    processed_invoice_data['invoice_number'] = invoice_post_data['invoice-number']
    processed_invoice_data['invoice_date'] = invoice_post_data['invoice-date']



    processed_invoice_data['dispdlts_name'] = invoice_post_data['dispdlts-name']
    processed_invoice_data['dispdlts_address1'] = invoice_post_data['dispdlts-address1']
    processed_invoice_data['dispdlts_address2'] = invoice_post_data['dispdlts-address2']
    processed_invoice_data['dispdlts_loc'] = invoice_post_data['dispdlts-loc']
    processed_invoice_data['dispdlts_pin'] = invoice_post_data['dispdlts-pin']
    processed_invoice_data['dispdlts_stcd'] = invoice_post_data['dispdlts-stcd']

    processed_invoice_data['shipdlts_gstin'] = invoice_post_data['shipdlts-gstin']
    processed_invoice_data['shipdlts_lglnm'] = invoice_post_data['shipdlts-lglnm']
    processed_invoice_data['shipdlts_trdnm'] = invoice_post_data['shipdlts-trdnm']
    processed_invoice_data['shipdlts_addr1'] = invoice_post_data['shipdlts-addr2']
    processed_invoice_data['shipdlts_addr2'] = invoice_post_data['shipdlts-addr1']
    processed_invoice_data['shipdlts_loc'] = invoice_post_data['shipdlts-loc']
    processed_invoice_data['shipdlts_pin'] = invoice_post_data['shipdlts-pin']
    processed_invoice_data['shipdlts_stcd'] = invoice_post_data['shipdlts-stcd']

    if 'igstcheck' in  invoice_post_data:
        processed_invoice_data['igstcheck'] = True
    else:
        processed_invoice_data['igstcheck'] = False

    processed_invoice_data['items'] = []
    processed_invoice_data['invoice_total_amt_without_gst'] = float(invoice_post_data['invoice-total-amt-without-gst'])
    processed_invoice_data['invoice_total_amt_sgst'] = float(invoice_post_data['invoice-total-amt-sgst'])
    processed_invoice_data['invoice_total_amt_cgst'] = float(invoice_post_data['invoice-total-amt-cgst'])
    processed_invoice_data['invoice_total_amt_igst'] = float(invoice_post_data['invoice-total-amt-igst'])
    processed_invoice_data['invoice_total_amt_with_gst'] = float(invoice_post_data['invoice-total-amt-with-gst'])


    invoice_post_data = dict(invoice_post_data)
    for idx, product in enumerate(invoice_post_data['invoice-product']):
        if product:
            print(idx, product)
            item_entry = {}
            item_entry['invoice_product'] = product
            item_entry['invoice_hsn'] = invoice_post_data['invoice-hsn'][idx]
            item_entry['invoice_unit'] = invoice_post_data['invoice-unit'][idx]
            item_entry['invoice_qty'] = int(invoice_post_data['invoice-qty'][idx])
            item_entry['invoice_rate_with_gst'] = float(invoice_post_data['invoice-rate-with-gst'][idx])
            item_entry['invoice_gst_percentage'] = float(invoice_post_data['invoice-gst-percentage'][idx])

            item_entry['invoice_rate_without_gst'] = float(invoice_post_data['invoice-rate-without-gst'][idx])
            item_entry['invoice_amt_without_gst'] = float(invoice_post_data['invoice-amt-without-gst'][idx])

            item_entry['invoice_amt_sgst'] = float(invoice_post_data['invoice-amt-sgst'][idx])
            item_entry['invoice_amt_cgst'] = float(invoice_post_data['invoice-amt-cgst'][idx])
            item_entry['invoice_amt_igst'] = float(invoice_post_data['invoice-amt-igst'][idx])
            item_entry['invoice_amt_with_gst'] = float(invoice_post_data['invoice-amt-with-gst'][idx])

            processed_invoice_data['items'].append(item_entry)

    print(processed_invoice_data)

    processed_invoice_data['itemslist'] = []
    invoice_post_data = dict(invoice_post_data)
    for idx, item in enumerate(invoice_post_data['invoice-item']):
        if item:
            print(idx, item)
            item_list_entry = {}
            item_list_entry['invoice_slno'] = invoice_post_data['invoice-slno'][idx]
            item_list_entry['invoice_prdesc'] = invoice_post_data['invoice_prdesc'][idx]
            item_list_entry['invoice_isservc '] = invoice_post_data['invoice-isservc '][idx]
            item_list_entry['invoice_hsncd'] = invoice_post_data['invoice-hsncd'][idx]
            item_list_entry['invoice_barcde'] = invoice_post_data['invoice-barcde'][idx]
            item_list_entry['invoice_qty'] = invoice_post_data['invoice-qty'][idx]
            item_list_entry['invoice_freeqty'] = invoice_post_data['invoice-freeqty'][idx]
            item_list_entry['invoice_unit'] = invoice_post_data['invoice-unit'][idx]
            item_list_entry['invoice_unitprice'] = invoice_post_data['invoice-unitprice'][idx]
            item_list_entry['invoice_totamt'] = invoice_post_data['invoice-totamt'][idx]
            item_list_entry['invoice_discount'] = invoice_post_data['invoice-discount'][idx]
            item_list_entry['invoice_pretaxval'] = invoice_post_data['invoice-pretaxval'][idx]
            item_list_entry['invoice_assamt'] = invoice_post_data['invoice-assamt'][idx]
            item_list_entry['invoice_gstrt'] = invoice_post_data['invoice-gstrt'][idx]
            item_list_entry['invoice_igstamt'] = invoice_post_data['invoice-igstamt'][idx]
            item_list_entry['invoice_cgstamt'] = invoice_post_data['invoice-cgstamt'][idx]
            item_list_entry['invoice_usgstamt'] = invoice_post_data['invoice-sgstamt'][idx]
            item_list_entry['invoice_cesrt'] = invoice_post_data['invoice-cesrt'][idx]
            item_list_entry['invoice_cesamt'] = invoice_post_data['invoice-cesamt'][idx]
            item_list_entry['invoice_cesnonadvlamt'] = invoice_post_data['invoice-cesnonadvlamt'][idx]
            item_list_entry['invoice_statecesrt'] = invoice_post_data['invoice-statecesrt'][idx]
            item_list_entry['invoice_statecesamt'] = invoice_post_data['invoice-statecesamt'][idx]
            item_list_entry['invoice_statecesnonadvlamt'] = invoice_post_data['invoice-statecesnonadvlamt'][idx]
            item_list_entry['invoice_othchrg'] = invoice_post_data['invoice-othchrg'][idx]
            item_list_entry['invoice_totitemval'] = invoice_post_data['invoice-totitemval'][idx]
            item_list_entry['invoice_ordlineref'] = invoice_post_data['invoice-ordlineref'][idx]
            item_list_entry['invoice_orgcntry'] = invoice_post_data['invoice-orgcntry'][idx]
            item_list_entry['invoice_prdslno'] = invoice_post_data['invoice-prdslno'][idx]



            item_list_entry['invoice_rate_without_gst'] = float(invoice_post_data['invoice-rate-without-gst'][idx])
            item_list_entry['invoice_amt_without_gst'] = float(invoice_post_data['invoice-amt-without-gst'][idx])

            item_list_entry['invoice_amt_sgst'] = float(invoice_post_data['invoice-amt-sgst'][idx])
            item_list_entry['invoice_amt_cgst'] = float(invoice_post_data['invoice-amt-cgst'][idx])
            item_list_entry['invoice_amt_igst'] = float(invoice_post_data['invoice-amt-igst'][idx])
            item_list_entry['invoice_amt_with_gst'] = float(invoice_post_data['invoice-amt-with-gst'][idx])

            processed_invoice_data['itemslist'].append(item_list_entry)

    print(processed_invoice_data)
    return processed_invoice_data

def update_products_from_invoice(invoice_data_processed, request):
    for item in invoice_data_processed['items']:
        new_product = False
        if Product.objects.filter(user=request.user,
                                  product_name=item['invoice_product'],
                                  product_hsn=item['invoice_hsn'],
                                  product_unit=item['invoice_unit'],
                                  product_gst_percentage=item['invoice_gst_percentage']).exists():
            product = Product.objects.get(user=request.user,
                                          product_name=item['invoice_product'],
                                          product_hsn=item['invoice_hsn'],
                                          product_unit=item['invoice_unit'],
                                          product_gst_percentage=item['invoice_gst_percentage'])
        else:
            new_product = True
            product = Product(user=request.user,
                              product_name=item['invoice_product'],
                              product_hsn=item['invoice_hsn'],
                              product_unit=item['invoice_unit'],
                              product_gst_percentage=item['invoice_gst_percentage'])
        product.product_rate_with_gst = item['invoice_rate_with_gst']
        product.save()

        if new_product:
            create_inventory(product)

def update_items_from_invoice(invoice_data_processed, request):
    for item in invoice_data_processed['itemslist']:
        new_item = False
        if Item.objects.filter(user=request.user,
                                  item_slno=item['invoice_slno'],
                                  item_prdesc=item['invoice_prdesc'],
                                  item_isservc=item['invoice_isservc'],
                                  item_hsncd=item['invoice_hsncd'],
                                  item_barcde=item['invoice_barcde'],
                                  item_qty=item['invoice_qty'],
                                  item_sfreeqty=item['invoice_freeqty'],
                                  item_unit=item['invoice_unit'],
                                  item_unitprice=item['invoice_unitprice'],
                                  item_totamt=item['invoice_totamt'],
                                  item_discount=item['invoice_discount'],
                                  item_pretaxval=item['invoice_pretaxval'],
                                  item_assamt=item['invoice_assamt'],
                                  item_gstrt=item['invoice_gstrt'],
                                  item_igstamt=item['invoice_igstamt'],
                                  item_cgstamt=item['invoice_cgstamt'],
                                  item_sgstamt=item['invoice_sgstamt'],
                                  item_cesrt=item['invoice_cesrt'],
                                  item_cesamt=item['invoice_cesamt'],
                                  item_cesnonadvlamt=item['invoice_cesnonadvlamt'],
                                  item_statecesrt=item['invoice_statecesrt'],
                                  item_statecesamt=item['invoice_statecesamt'],
                                  item_statecesnonadvlamt=item['invoice_statecesnonadvlamt'],
                                  item_othchrg=item['invoice_othchrg'],
                                  item_totitemval=item['invoice_totitemval'],
                                  item_ordlineref=item['invoice_ordlineref'],
                                  item_orgcntry=item['invoice_orgcntry'],
                                  item_prdslno=item['invoice_prdslno']).exists():
            item = Item.objects.get(user=request.user,
                                    item_slno=item['invoice_slno'],
                                    item_prdesc=item['invoice_prdesc'],
                                    item_isservc=item['invoice_isservc'],
                                    item_hsncd=item['invoice_hsncd'],
                                    item_barcde=item['invoice_barcde'],
                                    item_qty=item['invoice_qty'],
                                    item_sfreeqty=item['invoice_freeqty'],
                                    item_unit=item['invoice_unit'],
                                    item_unitprice=item['invoice_unitprice'],
                                    item_totamt=item['invoice_totamt'],
                                    item_discount=item['invoice_discount'],
                                    item_pretaxval=item['invoice_pretaxval'],
                                    item_assamt=item['invoice_assamt'],
                                    item_gstrt=item['invoice_gstrt'],
                                    item_igstamt=item['invoice_igstamt'],
                                    item_cgstamt=item['invoice_cgstamt'],
                                    item_sgstamt=item['invoice_sgstamt'],
                                    item_cesrt=item['invoice_cesrt'],
                                    item_cesamt=item['invoice_cesamt'],
                                    item_cesnonadvlamt=item['invoice_cesnonadvlamt'],
                                    item_statecesrt=item['invoice_statecesrt'],
                                    item_statecesamt=item['invoice_statecesamt'],
                                    item_statecesnonadvlamt=item['invoice_statecesnonadvlamt'],
                                    item_othchrg=item['invoice_othchrg'],
                                    item_totitemval=item['invoice_totitemval'],
                                    item_ordlineref=item['invoice_ordlineref'],
                                    item_orgcntry=item['invoice_orgcntry'],
                                    item_prdslno=item['invoice_prdslno'])
        else:
            new_item = True
            item = Item(user=request.user,
                                    item_slno=item['invoice_slno'],
                                    item_prdesc=item['invoice_prdesc'],
                                    item_isservc=item['invoice_isservc'],
                                    item_hsncd=item['invoice_hsncd'],
                                    item_barcde=item['invoice_barcde'],
                                    item_qty=item['invoice_qty'],
                                    item_sfreeqty=item['invoice_freeqty'],
                                    item_unit=item['invoice_unit'],
                                    item_unitprice=item['invoice_unitprice'],
                                    item_totamt=item['invoice_totamt'],
                                    item_discount=item['invoice_discount'],
                                    item_pretaxval=item['invoice_pretaxval'],
                                    item_assamt=item['invoice_assamt'],
                                    item_gstrt=item['invoice_gstrt'],
                                    item_igstamt=item['invoice_igstamt'],
                                    item_cgstamt=item['invoice_cgstamt'],
                                    item_sgstamt=item['invoice_sgstamt'],
                                    item_cesrt=item['invoice_cesrt'],
                                    item_cesamt=item['invoice_cesamt'],
                                    item_cesnonadvlamt=item['invoice_cesnonadvlamt'],
                                    item_statecesrt=item['invoice_statecesrt'],
                                    item_statecesamt=item['invoice_statecesamt'],
                                    item_statecesnonadvlamt=item['invoice_statecesnonadvlamt'],
                                    item_othchrg=item['invoice_othchrg'],
                                    item_totitemval=item['invoice_totitemval'],
                                    item_ordlineref=item['invoice_ordlineref'],
                                    item_orgcntry=item['invoice_orgcntry'])
        item.item_prdslno = item['invoice_prdslno']
        item.save()

        if new_item:
            create_inventory(item)


def create_inventory(product):
    if not Inventory.objects.filter(user=product.user, product=product).exists():
        new_inventory = Inventory(user=product.user, product=product)
        new_inventory.save()
        
def create_inventory(item):
    if not Inventory.objects.filter(user=item.user, item=item).exists():
        new_inventory = Inventory(user=item.user, item=item)
        new_inventory.save()


def update_inventory(invoice, request):
    invoice_data =  json.loads(invoice.invoice_json)
    for item in invoice_data['items']:
        product = Product.objects.get(user=request.user,
                                      product_name=item['invoice_product'],
                                      product_hsn=item['invoice_hsn'],
                                      product_unit=item['invoice_unit'],
                                      product_gst_percentage=item['invoice_gst_percentage'])
        inventory = Inventory.objects.get(user=product.user, product=product)
        change = int(item['invoice_qty'])*(-1)
        inventory_log = InventoryLog(user=product.user,
                                     product=product,
                                     date=datetime.datetime.now(),
                                     change=change,
                                     change_type=4,
                                     associated_invoice=invoice,
                                     description="Sale - Auto Deduct")
        inventory_log.save()
        inventory.current_stock += change
        inventory.last_log = inventory_log
        inventory.save()
def update_inventory(invoice, request):
    invoice_data =  json.loads(invoice.invoice_json)
    for item in invoice_data['itemslist']:
        item = Item.objects.get(user=request.user,
                                     item_slno=item['invoice_slno'],
                                    item_prdesc=item['invoice_prdesc'],
                                    item_isservc=item['invoice_isservc'],
                                    item_hsncd=item['invoice_hsncd'],
                                    item_barcde=item['invoice_barcde'],
                                    item_qty=item['invoice_qty'],
                                    item_sfreeqty=item['invoice_freeqty'],
                                    item_unit=item['invoice_unit'],
                                    item_unitprice=item['invoice_unitprice'],
                                    item_totamt=item['invoice_totamt'],
                                    item_discount=item['invoice_discount'],
                                    item_pretaxval=item['invoice_pretaxval'],
                                    item_assamt=item['invoice_assamt'],
                                    item_gstrt=item['invoice_gstrt'],
                                    item_igstamt=item['invoice_igstamt'],
                                    item_cgstamt=item['invoice_cgstamt'],
                                    item_sgstamt=item['invoice_sgstamt'],
                                    item_cesrt=item['invoice_cesrt'],
                                    item_cesamt=item['invoice_cesamt'],
                                    item_cesnonadvlamt=item['invoice_cesnonadvlamt'],
                                    item_statecesrt=item['invoice_statecesrt'],
                                    item_statecesamt=item['invoice_statecesamt'],
                                    item_statecesnonadvlamt=item['invoice_statecesnonadvlamt'],
                                    item_othchrg=item['invoice_othchrg'],
                                    item_totitemval=item['invoice_totitemval'],
                                    item_ordlineref=item['invoice_ordlineref'],
                                    item_orgcntry=item['invoice_orgcntry'],
                                    item_prdslno = item['invoice_prdslno'])
        inventory = Inventory.objects.get(user=item.user, item=item)
        change = int(item['invoice_qty'])*(-1)
        inventory_log = InventoryLog(user=item.user,
                                     item=item,
                                     date=datetime.datetime.now(),
                                     change=change,
                                     change_type=4,
                                     associated_invoice=invoice,
                                     description="Sale - Auto Deduct")
        inventory_log.save()
        inventory.current_stock += change
        inventory.last_log = inventory_log
        inventory.save()

def remove_inventory_entries_for_invoice(invoice, user):
        inventory_logs = InventoryLog.objects.filter(user=user,
                                     associated_invoice=invoice)
        for inventory_log in inventory_logs:
            inventory_product = inventory_log.product
            inventory_log.delete()
            inventory_obj = Inventory.objects.get(user=user, product=inventory_product)
            recalculate_inventory_total(inventory_obj, user)

def remove_inventory_entries_for_invoice(invoice, user):
        inventory_logs = InventoryLog.objects.filter(user=user,
                                     associated_invoice=invoice)
        for inventory_log in inventory_logs:
            inventory_item = inventory_log.item
            inventory_log.delete()
            inventory_obj = Inventory.objects.get(user=user, item=inventory_item)
            recalculate_inventory_total(inventory_obj, user)


def recalculate_inventory_total(inventory_obj, user):
    new_total = InventoryLog.objects.filter(user=user, product=inventory_obj.product).aggregate(Sum('change'))['change__sum']
    if not new_total:
        new_total = 0
    inventory_obj.current_stock = new_total
    inventory_obj.save()

def recalculate_inventory_total(inventory_obj, user):
    new_total = InventoryLog.objects.filter(user=user, item=inventory_obj.item).aggregate(Sum('change'))['change__sum']
    if not new_total:
        new_total = 0
    inventory_obj.current_stock = new_total
    inventory_obj.save()




