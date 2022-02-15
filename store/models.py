from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    model = getattr(instance, 'name')
    album_name = model.replace(' ', '_')
    return f'{album_name}/images/{filename}'


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    logo = models.FileField(upload_to='brand/')

    def __str__(self):
        return f'{self.brand_name}'


class ProductType(models.Model):
    type = models.CharField(max_length=15)
    value = models.CharField(max_length=15, default='')


    def __str__(self):
        return self.type


class ProductCategory(models.Model):
    type = models.ForeignKey(ProductType, related_name='product_type', on_delete=models.CASCADE)
    category = models.CharField(max_length=15)
    value = models.CharField(max_length=15, default='')


    def __str__(self):
        return f'{self.category} in {self.type.type}' 


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField()
    discounted_price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete = models.CASCADE)
    status = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    sold_quantity = models.IntegerField(default=0)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=20, default='', blank=True, null=True)


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)


    def __str__(self):
        return f'{self.name} {self.price}'


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to=get_upload_path)
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)

    def default(self):
        return self.images.filter(default=True).first()

    def thumbnails(self):
        return self.images.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return self.name

