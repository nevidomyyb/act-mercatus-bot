from time import sleep
import multiprocessing
import yfinance as yf

def run_loop_1():
    c = 0
    while True:
        print(f"Essa foi a iteração: {c} do loop 1")
        sleep(2)
        c+=1
        if c==100:
            break
    print("O loop 1 acabou")

def run_loop_2():
    c = 0
    while True:
        print(f"Essa foi a iteração: {c} do loop 2")    
        sleep(4)
        c+=1
        if c==35:
            break
        
    print("O loop 2 acabou")

# if __name__ == "__main__":
#     with multiprocessing.Manager() as manager:
#         processo1 = multiprocessing.Process(target=run_loop_1)
#         processo1.start()
        
#         processo2 = multiprocessing.Process(target=run_loop_2)
#         processo2.start()
        
#         processo1.join()
#         processo2.join()

def check_act(act_symbol):

    try:
        ticker = yf.Ticker(act_symbol)
        data = ticker.info
        return data
    except:
        print(f"{act_symbol} não encontrado")
        return False
    
print(check_act("BRL"))