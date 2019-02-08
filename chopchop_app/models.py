# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

# --- MODEL FOR BOOKING FORM -----------
class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    seat_num = models.IntegerField(blank=False, null=False)


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=15)
    table = models.ForeignKey(Table)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        unique_together = ["table", "start_time"]
        # pending item - prevent booking on the same timeslot & table


# --- MODEL FOR SENSOR DEMO ----------------

# Chair model
class Chair (models.Model):
    chair_code = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    current_session_time = models.DateTimeField(null=False, blank=False)
    current_session_id = models.IntegerField(blank=False, null=False, default=0)


#chair session model : for analytic

class ChairSession(models.Model):
    chair = models.ForeignKey(Chair)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=True, blank=True)
