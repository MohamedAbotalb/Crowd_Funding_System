# Generated by Django 5.0.4 on 2024-04-16 21:11

import apps.projects.models
import django.core.validators
import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_alter_customuser_phone_number'),
        ('categories', '0001_initial'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100, unique=True)),
                ('details', models.TextField()),
                ('total_target', models.IntegerField()),
                ('current_fund', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rate', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=20)),
                ('featured', models.BooleanField(default=False)),
                ('featured_at', models.DateTimeField(default=None, null=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='projects', to='categories.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.customuser')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(db_column='image', upload_to=apps.projects.models.project_picture_upload_path)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='projects.project')),
            ],
        ),
    ]
