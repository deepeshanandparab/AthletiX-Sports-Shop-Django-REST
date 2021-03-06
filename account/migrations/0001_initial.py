# Generated by Django 3.2.12 on 2022-03-03 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='images/profile/')),
                ('contact_number', models.IntegerField(blank=True, default=0, null=True)),
                ('alt_contact', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Home', max_length=20)),
                ('addr1', models.CharField(default='', max_length=200)),
                ('addr2', models.CharField(blank=True, max_length=200, null=True)),
                ('zipcode', models.IntegerField(default=0)),
                ('city', models.CharField(default='', max_length=200)),
                ('state', models.CharField(default='', max_length=200)),
                ('country', models.CharField(default='', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
