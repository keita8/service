# Generated by Django 3.2.9 on 2023-06-01 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0002_auto_20230601_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectview',
            name='user',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
    ]
