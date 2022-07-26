# Generated by Django 3.2.12 on 2022-03-31 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('kashmir_willow_bat', 'kashmir_willow_bat'), ('english_willow_bat', 'english_willow_bat'), ('tennis_bat', 'tennis_bat'), ('leather_ball', 'leather_ball'), ('batting_gloves', 'batting_gloves'), ('kit_bag_junior', 'kit_bag_junior'), ('tshirt', 'tshirt'), ('track_pant', 'track_pant'), ('cap', 'cap'), ('shoes', 'shoes')], default='', max_length=40),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=20, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_product', to='store.product')),
            ],
        ),
    ]