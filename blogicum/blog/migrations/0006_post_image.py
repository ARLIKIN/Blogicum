# Generated by Django 3.2.16 on 2023-11-26 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='birthdays_images', verbose_name='Фото'),
        ),
    ]
