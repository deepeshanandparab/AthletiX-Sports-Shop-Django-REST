# Generated by Django 3.2.12 on 2022-02-24 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20220224_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='expiring_on',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='starting_from',
            field=models.DateField(),
        ),
    ]
