import datetime
from django.core.management import BaseCommand
from event.models import Event
import vk_events
import fb_events


class Command(BaseCommand):

    ### to add extra arguments
    def add_arguments(self, parser):
       parser.add_argument('q', type=str)

    def handle(self, *args, **options):
        vk = vk_events.VkEvent()
        vk.handle(**options)
        fb = fb_events.FbEvent()
        fb.handle(**options)