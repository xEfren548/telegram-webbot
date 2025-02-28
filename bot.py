from telethon import TelegramClient, events
import asyncio
import aiohttp  # Para hacer solicitudes HTTP asíncronas
from datetime import datetime, timedelta
import pytz  # Para manejar zonas horarias
from dotenv import load_dotenv
import os
load_dotenv()




# Configuración
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number  = os.getenv('PHONE_NUMBER')
channel = -1001186547457
webhook_url = os.getenv('WEBHOOK_URL') # URL del servidor Node.js

client = TelegramClient("session", api_id, api_hash)

async def send_to_webhook(message, message_date):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json={"message": message, "date": message_date}) as response:
                if response.status == 200:
                    print("Mensaje enviado al servidor Node.js")
                else:
                    print(f"Error al enviar el mensaje: {response.status}")
        except Exception as e:
            print(f"Error en la solicitud HTTP: {e}")

''' Mensajes en tiempo real '''

async def main():
    await client.start(phone_number)  # Iniciar sesión
    me = await client.get_me()  # Obtener información de la cuenta
    print(f"Conectado como {me.username}")

    # Escuchar mensajes en tiempo real
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        message_text = event.message.text
        message_date = event.message.date

        utc_date = message_date.replace(tzinfo=pytz.UTC)  # Asegurar que la fecha esté en UTC
        local_date = utc_date.astimezone(pytz.timezone("America/Mexico_City"))
        formatted_date = local_date.strftime("%Y-%m-%d %H:%M:%S")


        print(f"Nuevo mensaje en {channel}: {formatted_date} el {message_date}")
        await send_to_webhook(message_text, formatted_date)  # Enviar mensaje al servidor Node.js

    await client.run_until_disconnected()

asyncio.run(main())


''' Obtener mensajes anteriores '''

# async def get_previous_messages():
#     try:
#         await client.start(PHONE_NUMBER)  # Iniciar sesión
#         me = await client.get_me()  # Obtener información de la cuenta
#         print(f"Conectado como {me.username}")

#         # Obtener la entidad del canal
#         try:
#             entity = await client.get_entity(CHANNEL)
#             print(f"Canal encontrado: {entity.title}")
#         except Exception as e:
#             print(f"No se pudo encontrar el canal: {e}")
#             return

#         # Calcular la fecha de hace X días
#         days_ago = 2  # Número de días atrás
#         from_date = datetime.now() - timedelta(days=days_ago)

#         # Obtener mensajes anteriores
#         messages = await client.get_messages(entity, offset_date=from_date, limit=10)  # Limitar a 10 mensajes
#         for message in messages:
#             print(f"Mensaje de {message.date}: {message.text}")
#             print(f"Fecha: {event.message}")

#             await send_to_webhook(message.text)  # Enviar mensaje al servidor Node.js

#     except Exception as e:
#         print(f"Error en el bot: {e}")
#     finally:
#         await client.disconnect()

# asyncio.run(get_previous_messages())