# -*- coding: utf-8 -*-

import facebook
import pprint
import config
from event.models import Event


class FbEvent():

    def __init__(self):
        self.count = 5000

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
            event['title'] = item['name']
            event['ext_id'] = item['id']
            event['photo'] = item['cover']['source'] \
                if 'cover' in item else ''
            try:
                save_event, created = Event.objects.update_or_create(**event)
                # print save_event.get_external_url()
            except Exception:
                pass

        if 'paging' in data:
            # time.sleep(0.5)
            options['after'] = data['paging']['cursors']['after']
            self.handle(**options)
