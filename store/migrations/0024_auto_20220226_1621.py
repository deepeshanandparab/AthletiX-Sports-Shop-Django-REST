# Generated by Django 3.2.12 on 2022-02-26 10:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0023_auto_20220224_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active'), ('expired', 'expired')], default='', max_length=40),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=10)),
                ('order_amount', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('coupon_used', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('discount_received', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('email', models.EmailField(default='', max_length=30)),
                ('addr1', models.TextField(default='', max_length=100)),
                ('addr2', models.TextField(default='', max_length=100)),
                ('pincode', models.CharField(default='', max_length=10)),
                ('country', models.CharField(default='', max_length=20)),
                ('delivery_method', models.CharField(default='standard', max_length=10)),
                ('contact', models.CharField(default='', max_length=10)),
                ('alt_contact', models.CharField(blank=True, max_length=10, null=True)),
                ('terms', models.CharField(default='accepted', max_length=10)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('complete', 'complete'), ('cancelled', 'cancelled')], default='pending', max_length=15)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
