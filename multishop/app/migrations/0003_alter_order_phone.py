# Generated by Django 4.1 on 2022-10-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.BigIntegerField(max_length=100),
        ),
    ]
