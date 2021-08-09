from django.contrib import admin


from .models import Dispdlts
from .models import Shipdlts
from .models import Invoice
from .models import Product
from .models import Item
from .models import UserProfile
from .models import BillingProfile
from .models import Inventory
from .models import InventoryLog



admin.site.register(UserProfile)
admin.site.register(BillingProfile)


admin.site.register(Dispdlts)
admin.site.register(Shipdlts)
admin.site.register(Invoice)
admin.site.register(Product)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(InventoryLog)
