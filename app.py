from telethon import events
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os
import multiprocessing
from mod.scheduler import send_message_routine
from time import sleep
import asyncio
from functools import partial
from sqlalchemy import create_engine
from base import Base
from mod.utils import create_string_by_monitored_actions, add_new_paper, check_and_add_to_user, perform_remove_paper
from typing import Dict

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
DATABASE_URL= os.getenv("DATABASE_URL")        


def create_fail_remove_paper_string(all_fails: Dict):
    string = """
    As respectivas ações não puderam ser removidas:
    """
    string = ["As respectivas ações não puderam ser removidas:"]
    
    for paper in all_fails:
        str_ = f"{paper}                motivo               {all_fails[paper][1]} não encontrado".center(70)
        string.append(str_)
        string_ = "\n".join(string)
    return string_
    

def run_client_scheduler(client_name: str):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)

    print("Segundo cliente rodando")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for c in range(10):
        print(f"Sending the {c}° messages.")
        # await send_message_routine(client, usuarios_interessados)
        TEST = ["...", ".."]
        partial_ = partial(send_message_routine, client, TEST)
        x = loop.run_until_complete(partial_())
        sleep(10)
        print("Messages sended.")
    loop.close()
    client.loop.stop()
    

def run_client(client_name: str):
    client = TelegramClient(client_name, api_id, api_hash)
    client.start(bot_token=bot_token)
    
    @client.on(events.NewMessage(pattern='/acao'))
    async def new_papers(event):
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
    async def check_papers(event):   
        user_id = event.message.peer_id.user_id
        rp = await check_and_add_to_user(user_id, client)
        acoes = create_string_by_monitored_actions(user_id)
        await client.send_message(user_id, f"Ações monitoradas atualmente: {acoes}")
        
    @client.on(events.NewMessage(pattern='/remover'))
    async def remove_paper(event):
        user_id = event.message.peer_id.user_id
        mensagem = event.raw_text
        palavras = mensagem.split()
        del palavras[0]
        successes, fails = perform_remove_paper(user_id, *palavras)
       
        response_string = ""
        if len(fails.keys()) != 0:
            fail_string = create_fail_remove_paper_string(fails)
            response_string+=fail_string
        if len(successes.keys()) != 0 :
            response_string+= f"\nAs seguintes ações foram removidas com sucesso: {', '.join(successes.keys())}"
        await client.send_message(user_id, response_string)
            
                
        # if remover_response:
        #     await client.send_message(user_id, f"As ações: {palavras} foram removidas.")
        # else:
        #     await client.send_message(user_id, f"Ocorreu algum erro.")
        
    client.run_until_disconnected()

if __name__ == "__main__":

    with multiprocessing.Manager() as manager:
        engine = create_engine(DATABASE_URL)
        ts =  Base.metadata.create_all(engine)
        
        telegram_process = multiprocessing.Process(target=run_client, args=('act_mercatus',))
        telegram_process.start()
        # telegram_process2 = multiprocessing.Process(target=run_client_scheduler, args=('act_scheduler',))
        # telegram_process2.start()
        
        telegram_process.join()
        # telegram_process2.join()
        