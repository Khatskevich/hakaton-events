# -*- coding: utf-8 -*-

import vk
import pprint
import config
from event.models import Event
from datetime import datetime as dt, timedelta
import time
import pytz


class VkEvent():

    # TODO: init count for get only one iterations
    def __init__(self):
        self.offset = 0
        self.count = 1000
        self.length = 0

    def handle(self, *args, **options):
        print "VK parsing..."
        session = vk.Session(access_token=config.VK_API_TOKEN)
        api = vk.API(session, v='5.40', lang='ru', timeout=100)
        fields = ['place', 'city', 'members_count', 'start_date']
        data = api.groups.search(q=options['q'],
                                 type='event',
                                 fields=','.join(fields),
                                 count=self.count,
                                 offset=self.offset,
                                 future=1)

        pp = pprint.PrettyPrinter(indent=1)
        # pp.pprint(data)

        if self.length == 0:
            self.length = data['count']

        for item in data['items']:
            #pp.pprint(item)
            event = Event()
            event.site = 'VK'
            event.lat = item['place']['latitude'] if 'place' in item else 0
            event.lng = item['place']['longitude'] if 'place' in item else 0
            if event.lat*event.lng == 0 :
                continue
            event.start_date = dt.fromtimestamp(item['start_date'], tz=pytz.utc) \
                if 'start_date' in item else None
            event.end_date = dt.fromtimestamp(item['end_date'], tz=pytz.utc) \
                if 'end_date' in item else event.start_date + timedelta(hours=2)
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['photo_200'] if 'photo_200' in item else 0
            event.description = item['description'] \
                if 'description' in item else ''
            event.member_count = item['member_count'] \
                if 'member_count' in item else 0
            event.create_or_update()
            """
            event = {}
            event['site'] = 'VK'
            event['lat'] = item['place']['latitude'] if 'place' in item else 0
            event['lng'] = item['place']['longitude'] if 'place' in item else 0
            if event['lat']*event['lng'] == 0 :
                continue
            event['start_date'] = str(dt.fromtimestamp(item['start_date'], tz=pytz.utc).strftime('YYYY-MM-DD HH:MM')) \
                if 'start_date' in item else ''
            event['end_date'] = str(dt.fromtimestamp(item['end_date'], tz=pytz.utc).strftime('YYYY-MM-DD HH:MM')) \
                if 'end_date' in item else ''
            print event['start_date']
            print event['end_date']
            event['title'] = item['name']
            event['ext_id'] = item['id']
            event['photo'] = item['photo_200'] if 'photo_200' in item else 0
            event['description'] = item['description'] \
                if 'description' in item else ''
            event['member_count'] = item['member_count'] \
                if 'member_count' in item else 0
            try:
                save_event, created = Event.objects.update_or_create(**event)
                # print save_event.get_external_url()
            except Exception, e:
                print e.message
            """

        if self.length > 0:
            self.offset += self.count
            self.length -= self.count
            time.sleep(0.5)
            self.handle(**options)
        else:
            print("VK parse ends.")
