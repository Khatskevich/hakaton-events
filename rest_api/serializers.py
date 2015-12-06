from rest_framework import serializers

from event.models import Event


class GetEventsSerializer(serializers.Serializer):
    lat_ne = serializers.FloatField(help_text="Latitude of the north east")
    lng_ne = serializers.FloatField(help_text="Longitude of the north east")
    lat_sw = serializers.FloatField(help_text="Latitude of the south west")
    lng_sw = serializers.FloatField(help_text="Longitude of the south west")



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # fields = ('__all__',)
        exclude = ( "id",)

class EventsSerializer(serializers.Serializer):
    events = EventSerializer(many=True)
