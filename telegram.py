import os
import asyncio
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler # administrar as mensagens do usuário
from pyrogram.types import Message # define os tipos de mensagem
from pyrogram.enums import ChatAction # ação do chat
from acessor import Acessor # agente

load_dotenv()

class TelegramBot:
    def __init__(self) -> None:
        logging.basicConfig( # configuração do logger
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.agentes = {} # Dicionário para armazenar os agentes por usuário

        self.app = Client( # cliente do telegram para interagir com o bot
            "InvAI_bot",
            api_id=os.getenv('TELEGRAM_API_ID'),
            api_hash=os.getenv('TELEGRAM_API_HASH'),
            bot_token=os.getenv('TELEGRAM_TOKEN')
        )
        
        self._setup_handle()

    def _setup_handle(self):
        start_handle = MessageHandler(
            self.start,
            filters.command("start") & filters.private
        )
        self.app.add_handler(start_handle)

        text_filter = filters.text & filters.private
        message_handler = MessageHandler(
            self.handle_message,
            text_filter
        )
        self.app.add_handler(message_handler)

        photo_filter = filters.photo & filters.private
        photo_handler = MessageHandler(
            self.handle_photo,
            photo_filter
        )
        self.app.add_handler(photo_handler)

    async def start(self, client: Client, message: Message): # função para iniciar a conversa de forma assíncrona
        await message.reply_text(
            "Olá! Eu sou o InvAI. Envie uma mensagem ou uma imagem para começarmos."
        )
        self.logger.info(f"Usuário {message.from_user.id} iniciou uma conversa.")
        
    async def handle_message(self, client: Client, message: Message): # função para tratar as mensagens do usuário de forma assíncrona
        user_id = message.from_user.id # id do usuário
        user_input = message.text # mensagem do usuário
        await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING) # apresentar a ação de digitando

        # Criar ou obter o agente existente para o usuário
        if user_id not in self.agentes:
            self.agentes[user_id] = Acessor(session_id=str(user_id))

        try:
            response = self.agentes[user_id].run(user_input)
        except Exception as err:
            self.logger.error(f"Erro ao processar a mensagem do usuário {user_id}: {err}", exc_info=True)
            response = "Desculpe, ocorreu um erro em telegram.py!"

        await message.reply_text(response)
        self.logger.info(f"Resposta enviada para o usuário {user_id}.")
        
    async def handle_photo(self, client: Client, message: Message): # função para tratar as imagens do usuário de forma assíncrona
        user_id = message.from_user.id # id do usuário
        await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING) # apresentar a ação de digitando

        storage_dir = os.path.join(os.getcwd(), 'storage')
        os.makedirs(storage_dir, exist_ok=True)

        photo_file_name = f"{user_id}_{message.photo.file_id}.jpg"
        photo_path = os.path.join(storage_dir, photo_file_name)
        await message.download(file_name=photo_path)

        # Criar ou obter o agente existente para o usuário
        if user_id not in self.agentes:
            self.agentes[user_id] = Acessor(session_id=str(user_id))

        try:
            response = self.agentes[user_id].run(photo_path)
        except Exception as err:
            self.logger.error(f"Erro ao processar a imagem do usuário {user_id}: {err}", exc_info=True)
            response = "Desculpe, ocorreu um erro em telegram.py!"

        await message.reply_text(response)
        self.logger.info(f"Resposta enviada para o usuário {user_id}.")
        
    def run(self):
        self.logger.info('InvAI iniciado!')
        self.app.run()