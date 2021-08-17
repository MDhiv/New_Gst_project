from django.forms import ModelForm

from .models import Dispdlts
from .models import Shipdlts
from .models import Product
from .models import Item
from .models import UserProfile


class DispdltsForm(ModelForm):
     class Meta:
         model = Dispdlts
         fields = ['dispdlts_name', 'dispdlts_address1', 'dispdlts_address2', 'dispdlts_loc', 'dispdlts_pin', 'dispdlts_stcd']

class ShipdltsForm(ModelForm):
     class Meta:
         model = Shipdlts
         fields = ['shipdlts_gstin', 'shipdlts_lglnm', 'shipdlts_trdnm', 'shipdlts_addr1', 'shipdlts_addr2','shipdlts_loc','shipdlts_pin', 'shipdlts_stcd']

class ProductForm(ModelForm):
     class Meta:
         model = Product
         fields = ['product_name', 'product_hsn', 'product_unit', 'product_gst_percentage', 'product_rate_with_gst']


class ItemForm(ModelForm):
     class Meta:
         model = Item
         fields = [
                 'item_slno', 
                 'item_prddesc', 
                 'item_isservc', 
                 'item_hsncd', 
                 'item_barcde', 
                 'item_qty', 
                 'item_freeqty', 
                 'item_unit', 
                 'item_unitprice', 
                 'item_totamt', 
                 'item_discount', 
                 'item_pretaxval', 
                 'item_assamt', 
                 'item_gstrt', 
                 'item_igstamt', 
                 'item_cgstamt', 
                 'item_sgstamt', 
                 'item_cesrt', 
                 'item_cesamt', 
                 'item_cesnonadvlamt', 
                 'item_statecesrt', 
                 'item_statecesamt', 
                 'item_statecesnonadvlamt', 
                 'item_othchrg', 
                 'item_totitemval', 
                 'item_ordlineref', 
                 'item_orgcntry', 
                 'item_prdslno', 
              ]


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['business_title'].required = True

    class Meta:
        model = UserProfile
        fields = ['business_title', 'business_address', 'business_email', 'business_phone', 'business_gst']

