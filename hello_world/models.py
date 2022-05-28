from django.db import models


class Guests(models.Model):
    class Meta:
        db_table = 'Guests'

    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    age = models.IntegerField()

    objects = models.Manager()


class Tables(models.Model):
    class Meta:
        db_table = 'Tables'

    number_of_seats = models.IntegerField()
    guest_id = models.IntegerField()

