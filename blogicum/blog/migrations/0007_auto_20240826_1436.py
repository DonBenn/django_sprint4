# Generated by Django 3.2.16 on 2024-08-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images', verbose_name='Фото'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
