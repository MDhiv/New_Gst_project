from django.contrib import admin


from .models import Dispdlts
from .models import Shipdlts
from .models import Product
from .models import Item
from .models import UserProfile
from .models import BillingProfile

admin.site.register(UserProfile)
admin.site.register(BillingProfile)
admin.site.register(Dispdlts)
admin.site.register(Shipdlts)
admin.site.register(Product)
admin.site.register(Item)

