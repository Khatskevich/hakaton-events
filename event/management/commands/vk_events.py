# -*- coding: utf-8 -*-

import vk
import pprint
import config
from django.core.management import BaseCommand
from event.models import Event
from datetime import datetime as dt


class Command(BaseCommand):

    def handle(self, *args, **options):
        session = vk.Session(access_token=config.VK_API_TOKEN)
        api = vk.API(session, v='5.40', lang='ru', timeout=10)
        fields = ['place', 'city', 'members_count', 'start_date']
        data = api.groups.search(q='Москва',
                                 type='event',
                                 fields=','.join(fields),
                                 count=1)

        # pp = pprint.PrettyPrinter(indent=1)
        # pp.pprint(data)

        for item in data['items']:
            event = Event()
            event.site = 'VK'
            event.lat = item['place']['latitude']
            event.lng = item['place']['longitude']
            event.start_date = dt.utcfromtimestamp(item['start_date'])
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['photo_200']
            # event.save()
            # print event.get_external_url()
