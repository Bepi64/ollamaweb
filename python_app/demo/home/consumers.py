import json
import asyncio
from ollama import AsyncClient
from channels.generic.websocket import AsyncWebsocketConsumer

class OllamaChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.pseudo = self.scope['url_route']['kwargs']['pseudo']
        self.model = self.scope['url_route']['kwargs']['model']
        self.client = AsyncClient(
                host='http://ollama:11434',
                )
        
        await self.accept()

    async def disconnect(self, close_code):
        pass 

    async def receive(self, text_data):

        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': "Format de message invalide."}))
            return

        message = (text_data_json.get('message') or '').strip()
        if not message:
            await self.send(text_data=json.dumps({'message': "Message vide."}))
            return

        await self.send(text_data=json.dumps({
            'type': 'stream_start',
            'message': ''
        }))

        await self.get_response_from_ollama(message)

        await self.send(text_data=json.dumps({
            'type': 'stream_end',
            'message': ''
        }))

    async def get_response_from_ollama(self, message):
        try:
            stream = await self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system', 
                        'content': "You're a helpful assistant who only answers in French."
                    },
                    {
                        'role': 'user', 
                        'content': message
                    }
                ],
                stream=True,
            )

            async for chunk in stream:
                if chunk.get('message', {}).get('content'):
                    content = chunk['message']['content']
                    await self.send(text_data=json.dumps({
                        'type': 'stream_chunk',
                        'message': content
                    }))
                    await asyncio.sleep(0.01)

        except Exception as exc:
            await self.send(text_data=json.dumps({
                'type': 'stream_error',
                'message': f"Erreur lors de l'appel à Ollama: {exc}"
            }))

