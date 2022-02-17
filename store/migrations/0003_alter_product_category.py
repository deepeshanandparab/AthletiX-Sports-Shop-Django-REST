# Generated by Django 3.2.12 on 2022-02-17 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('kwbat', 'kwbat'), ('ewbat', 'ewbat'), ('ball', 'ball'), ('batting_gloves', 'batting_gloves')], default='', max_length=15),
        ),
    ]
