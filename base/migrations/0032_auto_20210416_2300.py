# Generated by Django 3.1.7 on 2021-04-16 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_auto_20210416_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippmentorder',
            name='delivered',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]