from act import check_act

def create_string(user_data):
    str = "Últimas atualizações para seus papéis:\n"
    for act in user_data:
        str += f"{act}: R$ {user_data[act]}\n"
    return str

async def send_message_routine(client):
    from app import USUARIOS_INTERESSADOS
    prices = {}
    for usuario in USUARIOS_INTERESSADOS:
        for act in USUARIOS_INTERESSADOS[usuario]:
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
    for usuario in USUARIOS_INTERESSADOS:
        user_with_prices[usuario] = {}
        for act in prices:
            if act in USUARIOS_INTERESSADOS[usuario]:
                user_with_prices[usuario][act] = prices[act]
                
        string_message = create_string(user_with_prices[usuario])
        await client.send_message(usuario, string_message)