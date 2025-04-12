from utils.document_processing import loadAndSplitDoc
from utils.store_document import store_embeddings, drop_tables
from chardet.universaldetector import UniversalDetector
import tempfile
from models.pydantic_models import *
from utils.chat_summarizer import summarize
from schemas import schema
from sqlalchemy.orm import Session
from LLM.agent import agent_executor
import csv
import tiktoken

import logging


csvpath = 'keywords.csv'
logger = logging.getLogger()


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

# function to upload a file and create its embeddings
def handleUpload(file):
    content = file.file.read()

    detector = UniversalDetector()
    detector.feed(content)
    detector.close()
    encoding = detector.result['encoding']

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(content)
        file_path = temp_file.name
        file_type = file.content_type
        documents = loadAndSplitDoc(file_path, file_type, encoding)
        if(documents):
            logger.info(f'processed a document with {len(documents)} chunks')
            return store_embeddings(documents)

        
    return {'message':'something went wrong'}
    

# create a new chat session
def handleCreateSession(user_id:int, db :Session):
    new_session = schema.Session(user_id=user_id, summary="")
    logger.info(f'created a new session with for user {user_id}')
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# get all sessions for a user
def handleGetSessions(user_id:int, db:Session):
    return db.query(schema.Session).filter(schema.Session.user_id==user_id)


# create a new user
def handleCreateUser(user: UserBase, db :Session):
    new_user = schema.User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info('created a new user')
    return new_user


# get all chats for a session
def handleGetChatHistory(session_id:int, db: Session):
    return db.query(schema.ChatHistory).filter(schema.ChatHistory.session_id==session_id)


# get response for a query
def handleQuery(query: ChatHistoryBase, format:str, db: Session):
    session_id = query.session_id
    query_text = query.chat
    current_session = _getSession(session_id=session_id, db=db)

    if current_session is None:
        logger.info(f'no session for session id {session_id}')
        return {'message':f"Session with session id {session_id} does not exist!"}
    
    document_keywords=''
    with open(csvpath) as file:
        document_keywords = str(csv.reader(file))
    
    #update the summary for session
    chat_summary = current_session.summary

    #get response
    response = agent_executor.invoke({"input":query_text, "chat_history":chat_summary})

    input_tokens_used = num_tokens_from_string(query_text+chat_summary)
    output_tokens_used = num_tokens_from_string(str(response))

    new_summary = summarize(conv=response)
    current_session.summary = new_summary

    response['input_tokens_used'] = input_tokens_used
    response['output_tokens_used'] = output_tokens_used


    #format the response
    if format=='json':
        pass
    else :
        response = response['output'] + ' .. Input Tokens used :' + response['input_tokens_used'] + ' .. Output Tokens used :' + response['output_tokens_used']

    new_chat_instance = schema.ChatHistory(session_id=session_id, chat=str(response))
    db.add(new_chat_instance)
    db.commit()
    db.refresh(new_chat_instance)
    db.refresh(current_session)

    logger.info('responded to a new query')
    return new_chat_instance

            
def _updateSession(session:ChatSession, db: Session):
    pass


# get session by id
def _getSession(session_id:int, db: Session):
    return db.query(schema.Session).filter(schema.Session.session_id==session_id).first()