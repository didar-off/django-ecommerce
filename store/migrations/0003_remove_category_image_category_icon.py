# Generated by Django 4.2 on 2024-10-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_gallery_gallery_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='category/icons'),
        ),
    ]
