from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from base.models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/messages/',
        'GET /api/messages/:id',
        'GET /api/room-messages/:room',
        'POST /api/create-room',
        'DELETE /api/delete-room/:id',
        'PUT /api/update-room/:id',
        
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@login_required(login_url='login')
@api_view(['POST'])
def createRoom(request):
    if request.method == 'POST':
        serializer=RoomSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
        return Response(serializer.data)


@login_required(login_url='login')
@api_view(['GET','PUT'])
def updateRoom(request, pk):
    # if request.method ==
    if request.method == 'GET':
        room = Room.objects.get(id=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    if request.method == 'PUT':
        room = Room.objects.get(id=pk)
        serializer = RoomSerializer(room, data = request.data, partial = True)
        if(serializer.is_valid()):
            serializer.save()
        return Response(serializer.data)

@login_required(login_url='login')
@api_view(['DELETE'])
def deleteRoom(request, pk):
    if request.method == 'DELETE':
        room = Room.objects.get(id=pk)
        if request.user != room.host:
            return HttpResponse("Sorry, You Can't Update as you are NOT THE HOST of this room")
        room.delete()
        return HttpResponse("The room is deleted")

# @login_required(login_url='login')
# @api_view(['DELETE'])
# def deleteRoom(request, pk):
#     if request.method == 'DELETE':
#         room = Room.objects.get(id=pk)
#         room.delete()
#         return HttpResponse("The room is deleted")




@api_view(['GET'])
def getAllMessages(request):
    message = Message.objects.all()
    serializer = MessageSerializer(message, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request, pk):
    message = Message.objects.get(id = pk)
    serializer = MessageSerializer(message, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def getRoomMessages(request, pk):
    message = Message.objects.filter(room = pk)
    serializer = MessageSerializer(message, many = True)
    return Response(serializer.data)

# @api_view(['POST'])
