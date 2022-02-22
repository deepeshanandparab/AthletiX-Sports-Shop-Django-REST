from django.contrib import admin
from .models import Brand
from .models import Product
from .models import ImageAlbum
from .models import ProductType
from .models import Wishlist
from .models import BuyingPrice
from .models import CouponCode


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ImageAlbum)
admin.site.register(ProductType)
admin.site.register(Wishlist)
admin.site.register(BuyingPrice)
admin.site.register(CouponCode)
