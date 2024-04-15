# Generated by Django 5.0.4 on 2024-04-15 15:07

import apps.projects.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='pictures',
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='projectpicture',
            name='image',
            field=models.ImageField(db_column='image', upload_to=apps.projects.models.project_picture_upload_path),
        ),
        migrations.AlterField(
            model_name='projectpicture',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='projects.project'),
        ),
    ]