# -*- coding: utf-8 -*-

import vk
import pprint
import config
from django.core.management import BaseCommand
from event.models import Event
from datetime import datetime as dt
import time


class Command(BaseCommand):

    offset = 0
    count = 100
    length = 0

    def add_arguments(self, parser):
        parser.add_argument('q', type=str)

    def handle(self, *args, **options):
        session = vk.Session(access_token=config.VK_API_TOKEN)
        api = vk.API(session, v='5.40', lang='ru', timeout=100)
        fields = ['place', 'city', 'members_count', 'start_date']
        data = api.groups.search(q=options['q'],
                                 type='event',
                                 fields=','.join(fields),
                                 count=self.count,
                                 offset=self.offset)

        pp = pprint.PrettyPrinter(indent=1)
        # pp.pprint(data)   

        if self.length == 0:
            self.length = data['count']

        for item in data['items']:
            event = Event()
            event.site = 'VK'
            event.lat = item['place']['latitude'] if 'place' in item else 0
            event.lng = item['place']['longitude'] if 'place' in item else 0
            event.start_date = dt.utcfromtimestamp(item['start_date']) \
                if 'start_date' in item else ''
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['photo_200'] if 'photo_200' in item else 0
            # event.save()
            # print event.get_external_url()

        if self.length > 0:
            self.offset += self.count
            self.length -= self.count
            time.sleep(0.5)
            self.handle(**options)
