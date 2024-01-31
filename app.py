from telethon import events
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import multiprocessing
from mod.scheduler import create_schedule
# from apscheduler.triggers.interval import IntervalTrigger
# from mod.scheduler import create_scheduler

def create_string_by_monitored_actions(user_id):
    return ", ".join(usuarios_interessados[user_id])

async def check_and_add_to_user(user_id, client):
    if user_id not in usuarios_interessados.keys():
        usuarios_interessados[user_id] = []
        await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")
        return False
    

def run_client(client_dict, api_id, api_hash, bot_token, usuarios_interessados):
    with TelegramClient('act_mercatus', api_id, api_hash) as client:
        client.start(bot_token=bot_token)
        
        client_dict['session_path'] = 'act_mercatus'
        print(client_dict)
        
        @client.on(events.NewMessage(pattern='/acao'))
        async def nova_acao(event):
            mensagem = event.raw_text
            palavras = mensagem.split()
            user_id = event.message.peer_id.user_id
            rp = await check_and_add_to_user(user_id, client)
            if len(palavras) == 2:
                parametro = palavras[1]
                usuarios_interessados[user_id].append(parametro)
            else:
                parametros = palavras[1:]
                usuarios_interessados[user_id].extend(parametros)
            acoes = create_string_by_monitored_actions(user_id)
            await event.respond(f"As ações que vão ser monitoradas agora: {acoes}")

        @client.on(events.NewMessage(pattern='/check'))
        async def checar_acoes(event):   
            user_id = event.message.peer_id.user_id
            rp = await check_and_add_to_user(user_id, client)
            acoes = create_string_by_monitored_actions(user_id)
            await client.send_message(user_id, f"Ações monitoradas atualmente: {acoes}")
            
        client.run_until_disconnected()
    
        
if __name__ == "__main__":
    usuarios_interessados = {
    }

    load_dotenv()
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")

    print('tafora')
    with multiprocessing.Manager() as manager:
        print('entro aq')
        client_dict = manager.dict()
        
        telegram_process = multiprocessing.Process(target=run_client, args=(client_dict, api_id, api_hash, bot_token, usuarios_interessados))
        telegram_process.start()
        
        loop_process = multiprocessing.Process(target=create_schedule, args=(client_dict, api_id, api_hash, usuarios_interessados))
        loop_process.start()
        
        telegram_process.join()
        loop_process.join()
        