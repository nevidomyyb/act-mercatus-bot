import yfinance as yf
from sqlalchemy import (create_engine, text)
from sqlalchemy.orm import Session
from models import Act_User, User_Papers, Paper
from telethon.sync import TelegramClient


def check_act(act_symbol):
    if '.SA' not in act_symbol:
        act_symbol += '.SA'
    try:
        ticker = yf.Ticker(act_symbol)
        data = ticker.info
        return data
    except:
        print(f"{act_symbol} não encontrado")
        return False
    
def create_string_by_monitored_actions(user_id) -> str:
    from app import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        user = session.query(Act_User).filter(Act_User.telegram_user == user_id).first()
        
        sql_query = """
            SELECT act_user.user_id as user_id,
                act_user.telegram_user,
                paper.paper_id,
                paper.name_paper,
                paper.last_price
            FROM act_user
            JOIN user_papers ON act_user.user_id = user_papers.user_id
            JOIN paper ON user_papers.paper_id = paper.paper_id
            WHERE act_user.user_id = :user_id
        """
        result = session.execute(text(sql_query), {'user_id': user.user_id}).fetchall()
        string = ", ".join([row.name_paper for row in result])
        print(string)
        return string

def perform_remove_paper(user_id: str, *args: any):
    from app import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    fails = {}
    successes = {}
    with Session(engine) as session:
        user = session.query(Act_User).filter(Act_User.telegram_user == user_id).first()
        if not user: fails[paper] = [False, 'user']
        for paper in args:
            paper_instance = session.query(Paper).filter(Paper.name_paper == paper).first()
            if not paper_instance: 
                fails[paper] = [False, 'paper']
                continue
            paper_instance_holded_by_user = session.query(User_Papers).filter(
                User_Papers.paper_id == paper_instance.paper_id, 
                User_Papers.user_id == user.user_id
            ).first()
            if not paper_instance_holded_by_user: 
                fails[paper] = [False, 'holder']
                continue
            session.delete(paper_instance_holded_by_user)
            session.commit()
            successes[paper] = True
    return successes, fails

def add_new_paper(user_id: str, *args:any ) -> None:

    from app import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        user = session.query(Act_User).filter(Act_User.telegram_user == user_id).first()
        papers = []
        for act in args:
            boolean = check_act(act)
            if not boolean:
                continue
            paper_instance = session.query(Paper).filter(Paper.name_paper == act).first()
            if paper_instance:
                exist = session.query(User_Papers).filter(User_Papers.user_id == user.user_id, User_Papers.paper_id == paper_instance.paper_id).first()
                if not exist:
                    nova_third = User_Papers(user_id=user.user_id, paper_id=paper_instance.paper_id)
                    papers.append(nova_third)
                    print(f"O usuário {user_id} apenas adicionou a ação ao seu monitoramento")
            else:
                try:
                    last_price_ = boolean['currentPrice']
                except:
                    last_price_ = boolean['previousClose']
                    
                new_paper = Paper(name_paper=act, last_price=last_price_)
                session.add(new_paper)
                session.commit()
                nova_third = User_Papers(user_id=user.user_id, paper_id=new_paper.paper_id)
                papers.append(nova_third)
                print(f"O usuário {user_id} acabou criando o papel e adicionou ao seu monitoramento")
        session.add_all(papers)
        session.commit()
        
async def check_and_add_to_user(user_id: str, client: TelegramClient) -> bool:
    from app import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        user = session.query(Act_User).filter(Act_User.telegram_user == user_id).first()
        if not user:
            new_user = Act_User(telegram_user=user_id)
            session.add(new_user)
            session.commit()
            await client.send_message(user_id, f"Você foi inserido na lista de usuários do Act Mercatus.")
            return False