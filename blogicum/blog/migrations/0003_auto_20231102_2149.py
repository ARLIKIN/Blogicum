# Generated by Django 3.2.16 on 2023-11-02 17:49

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20231031_2340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]