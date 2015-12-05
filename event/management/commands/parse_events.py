import datetime
from django.core.management import BaseCommand
from event.models import Event


class Command(BaseCommand):

    ### to add extra arguments
    #def add_arguments(self, parser):
    #    parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        #count = options['count']
        events = Event.objects.all() # all events
        event = Event()#to get new instance
        event.lat = 5
        event.lng = 6
        event.time = datetime.datetime.now()
        #event.save() to save new ivent