# Generated by Django 2.2.1 on 2019-05-14 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmain', '0010_auto_20190514_0148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photoreaction',
            old_name='Gallery',
            new_name='Photo',
        ),
    ]
