# Generated by Django 3.1.7 on 2021-03-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210313_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
