# Generated by Django 3.2.9 on 2023-06-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='address',
            field=models.TextField(default='Taouya Petit Lac commune de Ratoma, Conakry République de Guinée', verbose_name='adresse'),
        ),
    ]