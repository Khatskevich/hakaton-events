from django.db import models


# Create your models here.
class Event(models.Model):
    lat = models.FloatField(help_text="Latitude of the center")
    lng = models.FloatField(help_text="Longitude of the center")
    beginning_time = models.DateTimeField(help_text="time of the beginning of the event")
