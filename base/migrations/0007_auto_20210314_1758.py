# Generated by Django 3.1.7 on 2021-03-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_item_qauntity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='qauntity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='qauntity',
            field=models.IntegerField(default=1),
        ),
    ]
