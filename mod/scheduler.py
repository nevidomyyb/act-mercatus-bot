from .utils import check_act
from time import sleep
from telethon.sync import TelegramClient


def create_string(user_data):
    str = "Últimas atualizações para seus papéis:\n"
    for act in user_data:
        str += f"{act}: R$ {user_data[act]}\n"
    return str


        
async def send_message_routine(client, usuarios_interessados):
    prices = {}
    print('Entrou aqui pelo menos')
    print(usuarios_interessados)
    # for usuario in usuarios_interessados:
    #     print('Agora entrou aqui rsrsrrs')
    #     for act in usuarios_interessados[usuario]:
    #         if act in prices.keys():
    #             continue
    #         all_data = check_act(act)
    #         if all_data is False: 
    #             print("It was not a valid paper")
    #             await client.send_message(usuario, f"A ação '{act}' não é um papel válido.\n Removendo-a.")
    #             continue
    #         try:
    #             prices[act] = all_data['currentPrice']
    #         except:
    #             prices[act] = all_data['previousClose']
    # user_with_prices = {}
    # for usuario in usuarios_interessados:
    #     user_with_prices[usuario] = {}
    #     for act in prices:
    #         if act in usuarios_interessados[usuario]:
    #             user_with_prices[usuario][act] = prices[act]
                
    #     string_message = create_string(user_with_prices[usuario])
    #     sleep(3)
    #     print(usuario)
    #     print(string_message)
    #     await client.send_message(usuario, string_message)