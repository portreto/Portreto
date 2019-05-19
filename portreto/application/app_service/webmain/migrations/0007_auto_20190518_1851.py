# Generated by Django 2.2.1 on 2019-05-18 18:51

from django.db import migrations, models
import webmain.storage


class Migration(migrations.Migration):

    dependencies = [
        ('webmain', '0006_auto_20190518_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='AlbumCover',
            field=models.ImageField(blank=True, default='album_cover/default.jpeg', null=True, storage=webmain.storage.ExternalStorage(), upload_to='album_cover/'),
        ),
    ]