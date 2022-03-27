# Generated by Django 3.2.12 on 2022-03-26 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('kashmir_willow_bat', 'kashmir_willow_bat'), ('english_willow_bat', 'english_willow_bat'), ('tennis_bat', 'tennis_bat'), ('leather_ball', 'leather_ball'), ('batting_gloves', 'batting_gloves'), ('kit_bag_junior', 'kit_bag_junior'), ('cricket_whites', 'cricket_whites'), ('white_tshirt', 'white_tshirt'), ('white_track', 'white_track'), ('tshirt', 'tshirt'), ('track_pant', 'track_pant')], default='', max_length=40),
        ),
    ]
