# Generated by Django 2.2.1 on 2019-05-13 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmain', '0003_auto_20190513_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='User',
            new_name='user',
        ),
    ]
