# Generated by Django 3.2.9 on 2023-05-30 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_digitalproductfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalproductfile',
            name='free',
            field=models.BooleanField(default=False, verbose_name='en telechargement libre ?'),
        ),
        migrations.AddField(
            model_name='digitalproductfile',
            name='user_required',
            field=models.BooleanField(default=False, verbose_name='proprietaire exigé'),
        ),
    ]
