from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_title = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(max_length=400, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    business_gst = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Plan(models.Model):
    plan_name = models.TextField(max_length=20, blank=True, null=True)
    plan_value = models.IntegerField(blank=True, null=True)
    # monthly_invoice_limit = models.IntegerField(blank=True, null=True)


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL)
    plan_start_date = models.DateField(blank=True, null=True)
    plan_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Dispdlts(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    dispdlts_name = models.CharField(max_length=200)
    dispdlts_address1 = models.TextField(max_length=300, blank=True, null=True)
    dispdlts_address2 = models.TextField(max_length=300, blank=True, null=True)
    dispdlts_loc = models.CharField(max_length=15, blank=True, null=True)
    dispdlts_pin = models.CharField(max_length=15, blank=True, null=True)
    dispdlts_stcd = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.dispdlts_name

class Shipdlts(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    shipdlts_gstin = models.CharField(max_length=20)
    shipdlts_lglnm = models.CharField(max_length=20)
    shipdlts_trdnm = models.CharField(max_length=20)
    shipdlts_addr1 = models.TextField(max_length=300, blank=True, null=True)
    shipdlts_addr2 = models.TextField(max_length=300, blank=True, null=True)
    shipdlts_loc = models.CharField(max_length=20)
    shipdlts_pin = models.CharField(max_length=20)
    shipdlts_stcd = models.CharField(max_length=20)

    def __str__(self):
        return self.shipdlts_gstin


class Product(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=200)
    product_hsn = models.CharField(max_length=50, null=True, blank=True)
    product_unit = models.CharField(max_length=50)
    product_gst_percentage = models.FloatField()
    product_rate_with_gst = models.FloatField()
    def __str__(self):
        return str(self.product_name)

class Item(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    item_slno = models.CharField(max_length=30)
    item_prddesc = models.CharField(max_length=30)
    item_isservc = models.CharField(max_length=30)
    item_hsncd = models.CharField(max_length=30)
    item_freeqty = models.CharField(max_length=30)
    item_qty = models.CharField(max_length=30)
    item_barcde = models.CharField(max_length=30)
    item_unit = models.CharField(max_length=30)
    item_unitprice = models.CharField(max_length=30)
    item_totamt = models.CharField(max_length=30)
    item_discount = models.CharField(max_length=30)
    item_pretaxval = models.CharField(max_length=30)
    item_assamt = models.CharField(max_length=30)
    item_gstrt = models.CharField(max_length=30)
    item_igstamt= models.CharField(max_length=30)
    item_cgstamt = models.CharField(max_length=30)
    item_sgstamt = models.CharField(max_length=30)
    item_cesrt = models.CharField(max_length=30)
    item_cesamt = models.CharField(max_length=30)
    item_cesnonadvlamt = models.CharField(max_length=30)
    item_statecesrt = models.CharField(max_length=30)
    item_statecesamt = models.CharField(max_length=30)
    item_statecesnonadvlamt = models.CharField(max_length=30)
    item_othchrg = models.CharField(max_length=30)
    item_totitemval = models.CharField(max_length=30)
    item_ordlineref = models.CharField(max_length=30)
    item_orgcntry = models.CharField(max_length=30)
    item_prdslno = models.CharField(max_length=30)

    def __str__(self):
        return str(self.item_slno)








