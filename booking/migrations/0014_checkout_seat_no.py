# Generated by Django 4.2.7 on 2023-12-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_remove_checkout_seat_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='seat_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]