# Generated by Django 4.2.7 on 2023-12-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_rename_extra_luggage_checkout_extra_luggage_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='each_luggage_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
