# Generated by Django 3.2.15 on 2022-09-09 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tables',
            name='guest_id',
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello_world.tables')),
            ],
            options={
                'db_table': 'Seats',
            },
        ),
        migrations.CreateModel(
            name='Seating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello_world.guests')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello_world.seats')),
            ],
            options={
                'db_table': 'Seating',
            },
        ),
    ]