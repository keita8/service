# Generated by Django 3.2.9 on 2023-05-28 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ecommerce.apps.blog.models
import mptt.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='titre')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('content', tinymce.models.HTMLField(verbose_name='contenu')),
                ('keywords', models.CharField(max_length=250, verbose_name='mot clé')),
                ('cover', models.ImageField(upload_to=ecommerce.apps.blog.models.blog_image_path, verbose_name='image')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date de creation')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('status', models.IntegerField(choices=[(0, 'Brouillon'), (1, 'Publié')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='redacteur')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='activé')),
            ],
            options={
                'verbose_name': 'Categorie',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='nom')),
                ('email', models.EmailField(max_length=254)),
                ('content', models.TextField(help_text='message', verbose_name='contenu')),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='publication')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blogpost', verbose_name='article')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='blog.category', verbose_name='categorie'),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='redacteur')),
            ],
        ),
    ]
