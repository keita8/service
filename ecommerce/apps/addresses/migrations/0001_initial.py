# Generated by Django 3.2.9 on 2023-06-09 12:39

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('livraison', 'Livraison'), ('facturation', 'Facturation')], max_length=150, verbose_name='adresse de')),
                ('lastname', models.CharField(blank=True, max_length=150, null=True, verbose_name='nom')),
                ('firstname', models.CharField(blank=True, max_length=150, null=True, verbose_name='prenom')),
                ('mobile_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='telephone')),
                ('street_address', models.CharField(blank=True, max_length=150, null=True, verbose_name='adresse')),
                ('message', models.TextField(blank=True, null=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile', verbose_name='client')),
            ],
            options={
                'verbose_name': "Adresse d'expédition",
                'verbose_name_plural': "Adresses d'expédition",
                'ordering': ('-id',),
            },
        ),
    ]
