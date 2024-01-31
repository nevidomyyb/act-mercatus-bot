from .act import check_act
from time import sleep
from telethon.sync import TelegramClient


def create_string(user_data):
    str = "Últimas atualizações para seus papéis:\n"
    for act in user_data:
        str += f"{act}: R$ {user_data[act]}\n"
    return str

def create_schedule(client_dict, api_id, api_hash, usuarios_interessados):
    print("Teste")
    sleep(10)
    session_path = client_dict.get('session_path')
    print(session_path)
    if session_path:
        with TelegramClient(session_path,api_id, api_hash) as client:
            while client.client.loop.is_running():
                send_message_routine(client, usuarios_interessados)
                print('Messages sended')
                sleep(2)
        
async def send_message_routine(client, usuarios_interessados):
    prices = {}
    for usuario in usuarios_interessados:
        for act in usuarios_interessados[usuario]:
            if act in prices.keys():
                continue
            all_data = check_act(act)
            if all_data is False: 
                await client.send_message(usuario, f"A ação '{act}' não é um papel válido.\n Removendo-a.")
                continue
            try:
                prices[act] = all_data['currentPrice']
            except:
                prices[act] = all_data['previousClose']
    user_with_prices = {}
    for usuario in usuarios_interessados:
        user_with_prices[usuario] = {}
        for act in prices:
            if act in usuarios_interessados[usuario]:
                user_with_prices[usuario][act] = prices[act]
                
        string_message = create_string(user_with_prices[usuario])
        sleep(5)
        await client.send_message(usuario, string_message)