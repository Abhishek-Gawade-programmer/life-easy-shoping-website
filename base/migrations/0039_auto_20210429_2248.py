# Generated by Django 3.1.7 on 2021-04-29 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_auto_20210429_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippmentorder',
            name='delivered_done_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shippmentorder',
            name='delivered',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
