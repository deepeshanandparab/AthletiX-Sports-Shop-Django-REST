from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile/', null=True, blank=True)
    contact_number = models.IntegerField(default=0, null=True, blank=True)
    alt_contact = models.CharField(max_length=10, null=True, blank=True, default='')
    
    def __str__(self):
        return f'{self.user.username} Profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Address(models.Model):
    title = models.CharField(max_length=20, default='Home')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addr1 = models.CharField(max_length=200, default='')
    addr2 = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.IntegerField(default=0)
    city = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200, default='')

    def __str__(self):
        return f'{self.user.username}\'s {self.title} Address'


def create_user_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)

post_save.connect(create_user_address, sender=User)