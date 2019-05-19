# Generated by Django 2.2.1 on 2019-05-16 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AlbumCover', models.ImageField(default='album_cover/default.jpeg', upload_to='album_cover/')),
                ('Name', models.CharField(max_length=50)),
                ('Description', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('UploadDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('GalleryOwner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Photo', models.ImageField(blank=True, default='photos/default.jpg', null=True, upload_to='photos/')),
                ('UploadDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Location', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('Description', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('Gallery', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='webmain.Gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProfilePhoto', models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')),
                ('RegisterDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('BirthDate', models.DateField(blank=True, null=True)),
                ('Bio', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('FirstName', models.CharField(default='', max_length=20)),
                ('LastName', models.CharField(default='', max_length=30)),
                ('Sex', models.CharField(choices=[('ML', 'ML'), ('FM', 'FM'), ('OC', 'OC'), ('NA', 'NA')], default='NA', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UpdateDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Photo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webmain.Photo')),
                ('User', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UpdateDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('Photo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webmain.Photo')),
                ('User', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GalleryReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UpdateDateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('Gallery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webmain.Gallery')),
                ('User', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GalleryComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UploadDateTime', models.DateTimeField(default=None, editable=False, null=True)),
                ('Comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('Gallery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webmain.Gallery')),
                ('User', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FollowCond1', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
                ('FollowCond2', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Friend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]