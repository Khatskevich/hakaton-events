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
            # 'cover',
            # 'description',
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
                'q': options['q'],
                'type': 'event',
                'limit': self.count,
                'since_date': 'currentTime',
                'fields': ','.join(fields),
                'after': '' if not 'after' in options else options['after'],
            },
        )
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(len(data['data']))

        for item in data['data']:
            event = Event()
            event.site = 'FB'
            event.lat = 0
            event.lng = 0
            if 'place' in item:
                event.lat = item['place']['location']['latitude'] \
                    if 'location' in item['place'] else 0
                event.lng = item['place']['location']['longitude'] \
                    if 'location' in item['place'] else 0
            if event.lat * event.lng == 0:
                continue
            event.start_date = item['start_time'] \
                if 'start_time' in item else ''
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['cover']['source'] \
                if 'cover' in item else ''
            # event.save()
            # print event.get_external_url()

        if 'paging' in data:
            # time.sleep(0.5)
            options['after'] = data['paging']['cursors']['after']
            self.handle(**options)

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