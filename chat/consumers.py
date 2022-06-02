import json
from  channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#  async def connect(self):
#   print('Connected')
#   self.room_group_name = 'Test-Room'
#   print(f'{self.channel_name} joined the room.')
  
#   await self.channel_layer.group_add(
#    self.room_group_name,
#    self.channel_name
#   )

#   await self.accept()
#   message = {
#    'type': 'name',
#    'name': f'{self.channel_name}'
#   }
#   await self.send(text_data=json.dumps(message))


#  async def disconnect(self, close_code):
#   print('Disconnected')
#   await self.channel_layer.group_discard(
#    self.room_group_name,
#    self.channel_name
#   )


#  async def receive(self, text_data):
#   receive_dict = json.loads(text_data)
#   message = receive_dict['message']
#   print(self.channel_name)

#   await self.channel_layer.group_send(
#    self.room_group_name,
#    {
#     'type': 'send.message',
#     'message': f'{self.channel_name} - {message}'
#    }
#   )
#   print('Received message - ', message)

  
#  async def send_message(self, event):
#   message = event['message']
#   newmessage = {
#    'type':'chat',
#    'message': f'{message}'
#   }

#   await self.send(text_data = json.dumps(newmessage))

# class VideoCalling(AsyncWebsocketConsumer):
#     async def connect(self):

#         self.room_group_name = 'Test-Room'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         message = {
#         'type': 'name',
#         'name': f'{self.channel_name}'
#         }

#         await self.accept()
#         await self.send(text_data=json.dumps(message))

#     async def disconnect(self, close_code):
        
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#         print('Disconnected!')
        

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         receive_dict = json.loads(text_data)
#         peer_username = receive_dict['peer']
#         action = receive_dict['action']
#         message = receive_dict['message']

#         print('Message received: ', message)

#         print('peer_username: ', peer_username)
#         print('action: ', action)
#         print('self.channel_name: ', self.channel_name)

#         if(action == 'new-offer') or (action =='new-answer'):
#             receiver_channel_name = receive_dict['message']['receiver_channel_name']

#             print('Sending to ', receiver_channel_name)

#             receive_dict['message']['receiver_channel_name'] = self.channel_name

#             await self.channel_layer.send(
#                 receiver_channel_name,
#                 {
#                     'type': 'send.sdp',
#                     'receive_dict': receive_dict,
#                 }
#             )

#             return

#         receive_dict['message']['receiver_channel_name'] = self.channel_name

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send.sdp',
#                 'receive_dict': receive_dict,
#             }
#         ) 

#     async def send_sdp(self, event):
#         receive_dict = event['receive_dict']

#         this_peer = receive_dict['peer']
#         action = receive_dict['action']
#         message = receive_dict['message']

#         await self.send(text_data=json.dumps({
#             'peer': this_peer,
#             'action': action,
#             'message': message,
#         }))


from channels.generic.websocket import AsyncJsonWebsocketConsumer

class VideoCalling(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive_json(self, content):
        if(content['command'] == 'join_room'):
            await self.channel_layer.group_add(content['room'],self.channel_name)
            print('added')
        elif(content['command'] == 'join'):
            await self.channel_layer.group_send(content['room'],{
                'type':'join.message',
            })
            
        elif(content['command'] == 'offer'):
            await self.channel_layer.group_send(content['room'],{
                'type':'offer.message',
                'offer':content['offer']
            })
        elif(content['command'] == 'answer'):
            await self.channel_layer.group_send(content['room'],{
                'type':'answer.message',
                'answer':content['answer']
            })
        elif(content['command'] == 'candidate'):
            await self.channel_layer.group_send(content['room'],{
                'type':'candidate.message',
                'candidate':content['candidate'],
                'iscreated':content['iscreated']
            })
    async def join_message(self,event):
        await self.send_json({
            'command':'join'
        })
    
    async def offer_message(self,event):
        await self.send_json({
            'command':'offer',
            'offer':event['offer']
        })
    
    async def answer_message(self,event):
        await self.send_json({
            'command':'answer',
            'answer':event['answer']
        })
    
    async def candidate_message(self,event):
        await self.send_json({
            'command':'candidate',
            'candidate':event['candidate'],
            'iscreated':event['iscreated']
        })