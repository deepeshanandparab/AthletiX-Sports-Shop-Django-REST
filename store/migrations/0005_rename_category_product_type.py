# Generated by Django 3.2.12 on 2022-02-17 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20220217_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='type',
        ),
    ]
