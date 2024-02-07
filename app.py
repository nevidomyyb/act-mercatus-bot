from telethon import events
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import multiprocessing
from mod.scheduler import send_message_routine
from time import sleep
import asyncio
from functools import partial
from sqlalchemy import (create_engine, text)
from sqlalchemy.orm import Session
from base import Base
from models import Act_User, Paper, User_Papers
from mod.utils import check_act, create_string_by_monitored_actions, add_new_paper

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
DATABASE_URL= os.getenv("DATABASE_URL")        
            
async def check_and_add_to_user(user_id: str, client: TelegramClient) -> bool:
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        user = session.query(Act_User).filter(Act_User.telegram_user == user_id).first()
        if not user:
            new_user = Act_User(telegram_user=user_id)
            session.add(new_user)
            session.commit()
            await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")
            return False

def run_client_scheduler(client_name: str, api_id: str, api_hash: str, bot_token: str):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)
    client.start()

    print("Segundo cliente rodando")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for c in range(10):
        print(f"Sending the {c}° messages.")
        # await send_message_routine(client, usuarios_interessados)
        partial_ = partial(send_message_routine, client)
        x = loop.run_until_complete(partial_())
        sleep(10)
        print("Messages sended.")
    loop.close()
    client.loop.stop()
    

def run_client(client_name: str, api_id: str, api_hash: str, bot_token: str):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)
    
    @client.on(events.NewMessage(pattern='/acao'))
    async def nova_acao(event):
        mensagem = event.raw_text
        palavras = mensagem.split()
        user_id = event.message.peer_id.user_id
        rp = await check_and_add_to_user(user_id, client)
        if len(palavras) == 2:
            parametro = palavras[1]
            # usuarios_interessados[user_id].append(parametro)
            add_new_paper(user_id, parametro)
        else:
            parametros = palavras[1:]
            # usuarios_interessados[user_id].extend(parametros)
            add_new_paper(user_id, *parametros)
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

    print(api_id, api_hash, bot_token)
    with multiprocessing.Manager() as manager:
        engine = create_engine(DATABASE_URL)
        ts =  Base.metadata.create_all(engine)
        
        telegram_process = multiprocessing.Process(target=run_client, args=('act_mercatus', api_id, api_hash, bot_token))
        telegram_process.start()
        # telegram_process2 = multiprocessing.Process(target=run_client_scheduler, args=('act_scheduler', api_id, api_hash, bot_token, engine))
        # telegram_process2.start()
        
        telegram_process.join()
        # telegram_process2.join()
        