from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from event.models import Event
from rest_api.serializers import GetEventsSerializer, EventSerializer


@api_view(['POST'])
def get_near_location(request):
    """
    ---
    request_serializer: GetEventsSerializer
    """
    if request.method != 'POST':
        return Response("", status=status.HTTP_400_BAD_REQUEST)
    print request.data
    serializer = GetEventsSerializer(data=request.data)
    if serializer.is_valid():
        sdata = serializer.data
        print sdata
        events = Event.objects.all()
        return Response(EventSerializer(events, many=True).data, status=status.HTTP_200_OK)
