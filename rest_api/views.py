from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from event.models import Event
from rest_api.serializers import GetEventsSerializer, GetEventSerializer,EventsSerializer, EventSerializer, EventFullSerializer


@api_view(['POST'])
def get_near_location(request):
    """
    ---
    response_serializer: EventsSerializer
    request_serializer: GetEventsSerializer
    """
    if request.method != 'POST':
        return Response("", status=status.HTTP_400_BAD_REQUEST)
    print request.data
    serializer = GetEventsSerializer(data=request.data)
    if serializer.is_valid():
        sdata = serializer.data
        print sdata
        events = Event.objects.all().filter(lat__lte=sdata['lat_ne'], lat__gte=sdata['lat_sw'] , lng__lte=sdata['lng_ne'], lng__gte=sdata['lng_sw'] )[0:100]
        return Response(  EventsSerializer({'events':events}).data , status=status.HTTP_200_OK)
        #return Response( ' { "events" : ' + json.dumps(EventSerializer(events, many=True).data) + ' } ' , status=status.HTTP_200_OK)


@api_view(['POST'])
def get(request):
    """
    ---
    response_serializer: EventFullSerializer
    request_serializer: GetEventSerializer
    """
    if request.method != 'POST':
        return Response("", status=status.HTTP_400_BAD_REQUEST)
    print request.data
    serializer = GetEventSerializer(data=request.data)
    if serializer.is_valid():
        sdata = serializer.data
        print sdata
        events = Event.objects.get(ext_id=sdata['ext_id'])
        return Response(  EventFullSerializer(events).data , status=status.HTTP_200_OK)
        #return Response( ' { "events" : ' + json.dumps(EventSerializer(events, many=True).data) + ' } ' , status=status.HTTP_200_OK)


