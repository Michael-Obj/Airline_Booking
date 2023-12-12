# Generated by Django 4.2.7 on 2023-11-04 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_trip_round_multi_trip_booking_arrival_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200, null=True)),
                ('seat_numbers', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='booking_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='airline_name',
        ),
        migrations.RemoveField(
            model_name='flight_class',
            name='business',
        ),
        migrations.RemoveField(
            model_name='flight_class',
            name='economy',
        ),
        migrations.RemoveField(
            model_name='flight_class',
            name='first_class',
        ),
        migrations.RemoveField(
            model_name='flight_status',
            name='awaiting_departure',
        ),
        migrations.RemoveField(
            model_name='flight_status',
            name='trip_cancelled',
        ),
        migrations.RemoveField(
            model_name='flight_status',
            name='trip_completed',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='best',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='cheapest',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='default',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='time_saver',
        ),
        migrations.RemoveField(
            model_name='trip_round',
            name='one_way',
        ),
        migrations.RemoveField(
            model_name='trip_round',
            name='round_trip',
        ),
        migrations.AddField(
            model_name='flight_class',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='flight_status',
            name='status',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='offer',
            name='name',
            field=models.CharField(blank=True, default='default', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='trip_round',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='contact',
            field=models.CharField(max_length=15),
        ),
        migrations.AddField(
            model_name='booking',
            name='airline',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booking.airline'),
        ),
    ]
