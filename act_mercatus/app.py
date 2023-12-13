from telethon import events
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os


USUARIOS_INTERESSADOS = {
}

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

def create_string_by_monitored_actions(user_id):
    return ", ".join(USUARIOS_INTERESSADOS[user_id])

def check_and_add_to_user(user_id):
    if user_id not in USUARIOS_INTERESSADOS.keys():
        USUARIOS_INTERESSADOS[user_id] = []
        return False
    

def create_client():
    client = TelegramClient('act_mercatus', API_ID, API_HASH)
    return client

if __name__ == '__main__':
    client = create_client()
    client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(pattern='/acao'))
    async def nova_acao(event):
        mensagem = event.raw_text
        palavras = mensagem.split()
        user_id = event.message.peer_id.user_id

        rp = check_and_add_to_user(user_id)
        if rp is False: await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")
            
            
        if len(palavras) == 2:
            parametro = palavras[1]
            
            USUARIOS_INTERESSADOS[user_id].append(parametro)
        else:
            parametros = palavras[1:]
            USUARIOS_INTERESSADOS[user_id].extend(parametros)
        acoes = create_string_by_monitored_actions(user_id)
        await event.respond(f"As ações que vão ser monitoradas agora: {acoes}")
    
    @client.on(events.NewMessage(pattern='/check'))
    async def checar_acoes(event):
        user_id = event.message.peer_id.user_id

        rp = check_and_add_to_user(user_id)
        if rp is False: await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")

        acoes = create_string_by_monitored_actions(user_id)
        await client.send_message(user_id, f"Ações monitoradas atualmente: {acoes}")

    client.run_until_disconnected()