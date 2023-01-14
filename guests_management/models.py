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
    table_name = models.CharField(max_length=15, null=True)
    description = models.CharField(max_length=100, null=True)

    objects = models.Manager()


class Seats(models.Model):
    class Meta:
        db_table = 'Seats'

    seat_number = models.IntegerField()
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)


class Seating(models.Model):
    class Meta:
        db_table = 'Seating'

    guest = models.ForeignKey(Guests, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
