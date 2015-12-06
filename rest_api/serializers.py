from rest_framework import serializers

from event.models import Event


class GetEventsSerializer(serializers.Serializer):
    lat = serializers.FloatField(help_text="Latitude of the center")
    lng = serializers.FloatField(help_text="Longitude of the center")
    radius = serializers.FloatField(help_text="Radius of search")



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # fields = ('__all__',)
        exclude = ( "id",)

class EventsSerializer(serializers.Serializer):
    events = EventSerializer(many=True)
