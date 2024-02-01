from telethon import events
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import multiprocessing
from mod.scheduler import send_message_routine
from time import sleep
import asyncio
from functools import partial
# from apscheduler.triggers.interval import IntervalTrigger
# from mod.scheduler import create_scheduler

def create_string_by_monitored_actions(user_id, usuarios_interessados):
    return ", ".join(usuarios_interessados[user_id])

async def check_and_add_to_user(user_id, client, usuarios_interessados):
    if user_id not in usuarios_interessados.keys():
        usuarios_interessados[user_id] = []
        await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")
        return False

def run_client_scheduler(client_name, api_id, api_hash, bot_token, usuarios_interessados):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)
    client.start()

    print("Segundo cliente rodando")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for c in range(10):
        print(f"Sending the {c}° messages.")
        # await send_message_routine(client, usuarios_interessados)
        partial_ = partial(send_message_routine, client, usuarios_interessados)
        x = loop.run_until_complete(partial_())
        sleep(10)
        print("Messages sended.")
    loop.close()
    client.loop.stop()
    

def run_client(client_name, api_id, api_hash, bot_token, usuarios_interessados):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)
    
    @client.on(events.NewMessage(pattern='/acao'))
    async def nova_acao(event):
        mensagem = event.raw_text
        palavras = mensagem.split()
        user_id = event.message.peer_id.user_id
        rp = await check_and_add_to_user(user_id, client, usuarios_interessados)
        if len(palavras) == 2:
            parametro = palavras[1]
            usuarios_interessados[user_id].append(parametro)
        else:
            parametros = palavras[1:]
            usuarios_interessados[user_id].extend(parametros)
        acoes = create_string_by_monitored_actions(user_id, usuarios_interessados)
        await event.respond(f"As ações que vão ser monitoradas agora: {acoes}")

    @client.on(events.NewMessage(pattern='/check'))
    async def checar_acoes(event):   
        user_id = event.message.peer_id.user_id
        rp = await check_and_add_to_user(user_id, client, usuarios_interessados)
        acoes = create_string_by_monitored_actions(user_id, usuarios_interessados)
        await client.send_message(user_id, f"Ações monitoradas atualmente: {acoes}")
    client.run_until_disconnected()

if __name__ == "__main__":

    load_dotenv()
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    print(api_id, api_hash, bot_token)
    with multiprocessing.Manager() as manager:
        
        usuarios_interessados = {}
        
        telegram_process = multiprocessing.Process(target=run_client, args=('act_mercatus', api_id, api_hash, bot_token, usuarios_interessados))
        telegram_process.start()
        telegram_process2 = multiprocessing.Process(target=run_client_scheduler, args=('act_scheduler', api_id, api_hash, bot_token, usuarios_interessados))
        telegram_process2.start()
        
        telegram_process.join()
        telegram_process2.join()
        