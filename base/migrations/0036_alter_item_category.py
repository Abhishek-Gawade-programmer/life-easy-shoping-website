# Generated by Django 3.2 on 2021-04-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_auto_20210417_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('A', 'Available'), ('NA', 'Not Available')], default='NA', max_length=2),
        ),
    ]