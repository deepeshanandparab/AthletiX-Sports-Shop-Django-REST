# Generated by Django 3.2.12 on 2022-02-22 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_couponcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]