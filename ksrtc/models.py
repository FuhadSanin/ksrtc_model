from django.db import models
from django.contrib.auth.models import User

class BusTrip(models.Model):
    vehicle_number = models.CharField(max_length=100, unique=True)
    trip = models.PositiveIntegerField()
    stations = models.JSONField(default=list)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Trip {self.trip} - {self.vehicle_number}"