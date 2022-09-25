# Generated by Django 3.2.15 on 2022-09-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=12)),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'Guests',
            },
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats', models.IntegerField()),
                ('guest_id', models.IntegerField()),
            ],
            options={
                'db_table': 'Tables',
            },
        ),
    ]
