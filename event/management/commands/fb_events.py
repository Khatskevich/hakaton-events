# -*- coding: utf-8 -*-
import dateutil.parser
import facebook
import pprint
from datetime import datetime as dt, timedelta
import config
from event.models import Event


class FbEvent():

    def __init__(self):
        self.count = 5000

    def handle(self, *args, **options):
        print "FB parsing..."
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
            'category',
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
        # pp.pprint(data)

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
            if not 'start_time' in item:
                continue
            event.start_date = dateutil.parser.parse(item['start_time'])#dt.strptime(item['start_time'],'%Y-%m-%dT%H:%M:%S%Z')
            event.end_date = dateutil.parser.parse(item['end_time']) \
                if 'end_time' in item else event.start_date + timedelta(hours=2)
            event.title = item['name']
            event.ext_id = item['id']
            event.photo = item['cover']['source'] \
                if 'cover' in item else ''
            event.description = item['description'] \
                if 'description' in item else ''
            event.member_count = item['attending_count'] \
                if 'attending_count' in item else ''
            event.category = item['category'] \
                if 'category' in item else ''
            event.create_or_update()
            """
            event = {}
            event['site'] = 'FB'
            event['lat'] = 0
            event['lng'] = 0
            if 'place' in item:
                event['lat'] = item['place']['location']['latitude'] \
                    if 'location' in item['place'] else 0
                event['lng'] = item['place']['location']['longitude'] \
                    if 'location' in item['place'] else 0
            if event['lat'] * event['lng'] == 0:
                continue
            event['start_date'] = item['start_time'] \
                if 'start_time' in item else ''
            event['end_date'] = item['end_time'] \
                if 'end_time' in item else ''
            event['title'] = item['name']
            event['ext_id'] = item['id']
            event['photo'] = item['cover']['source'] \
                if 'cover' in item else ''
            event['description'] = item['description'] \
                if 'description' in item else ''
            event['member_count'] = item['attending_count'] \
                if 'attending_count' in item else ''
            event['category'] = item['category'] \
                if 'category' in item else ''
            try:
                save_event, created = Event.objects.update_or_create(**event)
                # print save_event.get_external_url()
            except Exception, e:
                print e.message
                pass
            """
        if 'paging' in data:
            # time.sleep(0.5)
            options['after'] = data['paging']['cursors']['after']
            self.handle(**options)
        else:
            print("FB parser ends.")
