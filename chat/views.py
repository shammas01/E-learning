import json
from django.shortcuts import render
from .models import Message
from django.http import HttpResponse
# Create your views here.

def index(request):
  return render(request, 'chatindex.html')


def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
#   messages = Message.objects.filter(room=room_name)[0:25]
   
    return render(request, 'room.html', {'room_name': room_name, 'username': username})
  



# Receive message from WebSocket
async def receive(self, text_data):
  data = json.loads(text_data)
  message = data['message']
  username = data['username']
  room = data['room']

  # Send message to room group
  await self.channel_layer.group_send(
    self.room_group_name,
    {
      'type': 'chat_message',
      'message': message,
      'username': username
    }
  )


