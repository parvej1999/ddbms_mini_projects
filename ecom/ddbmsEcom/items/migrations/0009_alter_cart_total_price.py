# Generated by Django 4.1.13 on 2023-11-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
