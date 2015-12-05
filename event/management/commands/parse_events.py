import datetime
from django.core.management import BaseCommand
from event.models import Event


class Command(BaseCommand):
    events = Event.objects.all() # all events
    event = Event()#to get new instance
    event.lat = 5
    event.lng = 6
    event.time = datetime.datetime.now()
    #event.save() to save new ivent
