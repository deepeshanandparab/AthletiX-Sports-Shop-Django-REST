# Generated by Django 3.2.12 on 2022-02-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20220217_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('kashmir_willow_bat', 'kashmir_willow_bat'), ('english_willow_bat', 'english_willow_bat'), ('leather_ball', 'leather_ball'), ('batting_gloves', 'batting_gloves'), ('kit_bag_junior', 'kit_bag_junior')], default='', max_length=40),
        ),
    ]