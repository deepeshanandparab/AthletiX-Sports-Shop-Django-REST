from re import M
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


COUPON_CODE_CHOICES = (
    ('inactive','inactive'),
    ('active','active'),
    ('expired','expired')
)

ORDER_STATUS_CHOICES = (
    ('pending','pending'),
    ('complete','complete'),
    ('cancelled','cancelled')
)

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
    type = models.CharField(max_length=30)
    value = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.type


TYPE_CHOICES = (
    ('kashmir_willow_bat','kashmir_willow_bat'),
    ('english_willow_bat','english_willow_bat'),
    ('tennis_bat','tennis_bat'),
    ('leather_ball','leather_ball'),
    ('batting_gloves','batting_gloves'),
    ('kit_bag_junior','kit_bag_junior'),
    ('tshirt','tshirt'),
    ('track_pant','track_pant'),
    ('cap','cap'),
    ('shoes','shoes')
)

SLEEVES_CHOICES = (
    ('half_sleeves', 'half_sleeves'),
    ('full_sleeves', 'full_sleeves'),
    ('sleeveless', 'sleeveless')
)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField()
    discounted_price = models.IntegerField(null=True, blank=True)
    summary = models.CharField(max_length=1000, default='')
    description = models.CharField(max_length=5000)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete = models.CASCADE)
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=50, default='', null=True, blank=True)
    type = models.CharField(max_length=40, choices=TYPE_CHOICES, default='')
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
        return f'({self.id}) {self.name} at MRP {self.price} in Stock {self.stock_quantity}'


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name='stock_product', on_delete=models.CASCADE)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    sleeves = models.CharField(max_length=20, choices=SLEEVES_CHOICES, default='', null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} size {self.size}, color {self.color}, \
        sleeves {self.sleeves} - {self.stock_quantity} stock left'  


class BuyingPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buying_price = models.IntegerField()


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


class Wishlist(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_product')
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='wishlist_user')

    def __str__(self):
        return f'{self.user_id} wishlisted product : {self.product_id.name}'
        

class RatingReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating_product')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='rating_user')
    rating = models.FloatField()
    review = models.TextField(max_length=200, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return f'{self.user} rated {self.product.name} with {self.rating} stars'


class CouponCode(models.Model):
    code = models.CharField(max_length=20, default='')
    discount = models.IntegerField(default=0)
    redeem_count = models.IntegerField(default=1)
    redeem_by = models.ManyToManyField(User, blank=True)
    applicable_on = models.ManyToManyField(Product, blank=True)
    starting_from = models.DateField()
    expiring_on = models.DateField()
    status = models.CharField(max_length=40, choices=COUPON_CODE_CHOICES, default='')

    def __str__(self):
        return f'{self.code} active duration between {self.starting_from} to {self.expiring_on} - {self.status}'



class Order(models.Model):
    order_id = models.CharField(max_length=10, default='')
    order_amount = models.FloatField()
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    coupon_used = models.CharField(max_length=10, default='', null=True, blank=True)
    discount_received = models.IntegerField(null=True, blank=True)
    delivery_method = models.CharField(max_length=10, default='standard')
    terms = models.CharField(max_length=10, default='accepted')
    date = models.DateField(default=datetime.today)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order: ({self.order_id}) {self.product.name}({self.quantity}) - {self.price} \
                        on {self.date}'


    def __unicode__(self):
        return u'%s %s' % (self.price, self.date)


