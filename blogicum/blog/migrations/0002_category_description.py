# Generated by Django 3.2.16 on 2024-07-31 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=0, verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
