# -*- coding: utf-8 -*-

import facebook
import pprint
import config
from django.core.management import BaseCommand
from event.models import Event
import time


class Command(BaseCommand):

    offset = 0
    count = 5000
    length = 0

    def add_arguments(self, parser):
        parser.add_argument('q', type=str)

    def handle(self, *args, **options):
        graph = facebook.GraphAPI(access_token=config.FB_API_TOKEN)
        fields = [
            'id',
            'name',
            'cover',
            'description',
            'start_time',
            'end_time',
            'place',
            'attending_count',
            'maybe_count',
            'interested_count',
        ]
        data = graph.request(
            "v2.5/search",
            {
                'q': 'Москва',
                'type': 'event',
                'limit': count,
                'since_date': 'currentTime',
                'fields': ','.join(fields),
            },
        )
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(data)

        for item in data['data']:
            event = Event()
            event.site = 'FB'
            event.lat = item['place']['location']['latitude'] if 'place' in item else 0
            event.lng = item['place']['location']['longitude'] if 'place' in item else 0
            event.start_date = item['start_time'] if 'start_time' in item else ''
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['cover']['source'] if 'cover' in item else 0
            # event.save()
            # print event.get_external_url()

# Parsing API:
'''
graph = facebook.GraphAPI(access_token=config.FB_API_TOKEN)
fields = ['id', 'name', 'cover', 'description', 'start_time', 'end_time', 'place', 'attending_count', 'maybe_count']
data = graph.request(
    "v2.5/search",
    {
        'q': 'Москва',
        'type': 'event',
        'limit': 5000,
        'since_date': 'currentTime',
        'fields': ','.join(fields),
    },
)
pp = pprint.PrettyPrinter(indent=1)
pp.pprint(data)
'''
