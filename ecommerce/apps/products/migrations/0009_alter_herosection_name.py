# Generated by Django 3.2.9 on 2023-06-01 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20230601_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herosection',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='titre'),
        ),
    ]
