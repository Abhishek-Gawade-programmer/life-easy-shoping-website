# Generated by Django 3.1.7 on 2021-04-17 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_auto_20210417_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='image4',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='image5',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='item',
            name='image6',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
