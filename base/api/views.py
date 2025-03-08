# from django.http import JsonResponse

from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


# we can use function based views or class based views if using restframework

@api_view(['GET','POST'])    # in api_view(here we pass http methods which can access the api)
def getRoutes(request):
    routes= [
        'GET api/',
        'GET api/rooms',
        'GET api/rooms/:id'
    ]
    # return JsonResponse(routes,safe=False)
    return Response(routes)



# you can remove the comments and comment new things and then run it to see the difference in working with rest framework and not working with rest framework .

# rest framework provide UI and a kind of form in which we can select which type data should be returned and can pass the body from that form to see the response .

# to get a all the rooms using id for anyone who wants to use this api in their projects etc
'''
@api_view(['GET'])
def getRooms(response):
    rooms=Room.objects.all()
    return Response(rooms)

'''
# Object of type Room is not JSON serializable 
# this error we will see if we go to the url because it is in the form of an object (Room.'objects'.all()) and no python object is allowed or can be parsed or automatically converted in json fromat . That is why we use serializers so that this error do not occur and serializer covert everything in json format if we try to use models etc .


# to get a all the rooms using id for anyone who wants to use this api in their projects etc
@api_view(['GET'])
def getRooms(response):
    rooms=Room.objects.all()
    serializer=RoomSerializer(rooms,many=True)  # here we pass the data which we want to serialize , if it is more than one thing then set ' many=True '
    return Response(serializer.data)    # we don't want to pass an object , we want to pass data that is why we have used serializer.data because serializer will return only object

    # if we don't pass serializer.data , we only pass serializer like Response(serializer) then -->>  Object of type ListSerializer is not JSON serializable


# to get a particular room using id for anyone who wants to use this api in their projects etc
@api_view(['GET'])
def getRoom(response,pk):
    room=Room.objects.get(id=pk)
    serializer=RoomSerializer(room) 
    return Response(serializer.data) 