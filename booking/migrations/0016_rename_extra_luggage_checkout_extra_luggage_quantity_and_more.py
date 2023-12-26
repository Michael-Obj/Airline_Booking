# Generated by Django 4.2.7 on 2023-12-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_flight_letter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='extra_luggage',
            new_name='extra_luggage_quantity',
        ),
        migrations.AlterField(
            model_name='booking',
            name='stops',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
