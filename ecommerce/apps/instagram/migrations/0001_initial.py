# Generated by Django 3.2.9 on 2023-06-09 12:39

from django.db import migrations, models
import ecommerce.apps.instagram.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('link', models.URLField()),
                ('image', models.ImageField(upload_to=ecommerce.apps.instagram.models.upload_insta_image_path)),
            ],
        ),
    ]
