# Generated by Django 3.2.10 on 2022-05-28 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello_world', '0006_auto_20220528_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seating',
            old_name='guest_id',
            new_name='guest',
        ),
        migrations.RenameField(
            model_name='seating',
            old_name='seat_id',
            new_name='seat',
        ),
        migrations.RenameField(
            model_name='seats',
            old_name='table_id',
            new_name='table',
        ),
    ]