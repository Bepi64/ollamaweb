import json
import asyncio
from ollama import AsyncClient
from channels.generic.websocket import AsyncWebsocketConsumer

class OllamaChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Récupérer le pseudo et le modèle depuis l'URL
        self.pseudo = self.scope['url_route']['kwargs']['pseudo']
        self.model = self.scope['url_route']['kwargs']['model']
        self.client = AsyncClient(
                host='http://ollama:11434',
                )
        
        # Accepter la connexion WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe lorsque la connexion est fermée
        pass 

    async def receive(self, text_data):
        # Réception d'un message envoyé par le client WebSocket
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': "Format de message invalide."}))
            return

        message = (text_data_json.get('message') or '').strip()
        if not message:
            await self.send(text_data=json.dumps({'message': "Message vide."}))
            return

        # Envoyer un message de début de streaming
        await self.send(text_data=json.dumps({
            'type': 'stream_start',
            'message': ''
        }))

        # Envoyer la requête à Ollama en streaming
        await self.get_response_from_ollama(message)

        # Envoyer un message de fin de streaming
        await self.send(text_data=json.dumps({
            'type': 'stream_end',
            'message': ''
        }))

    async def get_response_from_ollama(self, message):
        try:
            # Appel streaming à l'API locale d'Ollama
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

            # Envoyer chaque chunk au client
            async for chunk in stream:
                if chunk.get('message', {}).get('content'):
                    content = chunk['message']['content']
                    await self.send(text_data=json.dumps({
                        'type': 'stream_chunk',
                        'message': content
                    }))
                    # Petit délai pour éviter de surcharger
                    await asyncio.sleep(0.01)

        except Exception as exc:
            await self.send(text_data=json.dumps({
                'type': 'stream_error',
                'message': f"Erreur lors de l'appel à Ollama: {exc}"
            }))

