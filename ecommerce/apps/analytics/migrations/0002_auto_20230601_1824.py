# Generated by Django 3.2.9 on 2023-06-01 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objectview',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Article consulté', 'verbose_name_plural': 'Articles consultés'},
        ),
        migrations.AlterField(
            model_name='objectview',
            name='user',
            field=models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
    ]
