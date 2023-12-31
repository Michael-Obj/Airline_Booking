# Generated by Django 4.2.7 on 2023-11-04 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_remove_checkout_gender_female_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='depart_from',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='booking_depart_from', to='booking.location'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='destination',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='booking_destination', to='booking.location'),
        ),
    ]
