# Generated by Django 3.1.7 on 2021-04-16 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0028_auto_20210415_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippmentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered', models.DateTimeField()),
                ('verify_order', models.BooleanField(default=False)),
                ('payment_done', models.BooleanField(default=False)),
                ('payment_done_date', models.DateTimeField()),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ShippmentOrder',
                'verbose_name_plural': 'ShippmentOrders',
            },
        ),
    ]
