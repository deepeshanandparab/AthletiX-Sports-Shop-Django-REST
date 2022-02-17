from django.contrib import admin
from .models import Brand
from .models import Product
from .models import ImageAlbum
from .models import ProductType


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ImageAlbum)
admin.site.register(ProductType)
