# Generated by Django 4.2.7 on 2023-11-04 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_location_alter_booking_depart_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.TextField(null=True),
        ),
    ]
