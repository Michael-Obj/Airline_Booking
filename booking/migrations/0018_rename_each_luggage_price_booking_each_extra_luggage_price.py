# Generated by Django 4.2.7 on 2023-12-26 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0017_booking_each_luggage_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='each_luggage_price',
            new_name='each_extra_luggage_price',
        ),
    ]
