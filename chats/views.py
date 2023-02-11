from django.shortcuts import render, redirect
from chats.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
  return render(request, 'home.html')

def room(request, room):
  username = request.GET.get('username')
  room_details = Room.objects.get(name=room)
  return render(request, 'room.html', {
    'username': username,
    'room': room,
    'room_details': room_details
  })

# Used to check if room already exists, if yes then enter the same room elso create new room 
def checkview(request):
  room = request.POST['room_name']
  username = request.POST['username'] 

  if Room.objects.filter(name=room).exists():
    return redirect('/' + room + '/?username=' + username)

  else:
    new_room = Room.objects.create(name=room)
    new_room.save()
    return redirect('/' + room + '/?username=' + username)

# Used to store the data in the database
def send(request):
  message = request.POST['message']
  username = request.POST['username']
  room_id = request.POST['room_id']

  new_message = Message.objects.create(value=message, user=username, room=room_id)
  new_message.save()

  return HttpResponse('Message sent successfully')

# Using the room name get all the messages of the room and return a json response of all the messages.
# In the frontend we will use ajax to access that json response and display it to the user.
def getMessages(reguest, room):
  room_details = Room.objects.get(name=room)
  messages = Message.objects.filter(room=room_details.id)
  return JsonResponse({"messages": list(messages.values())})