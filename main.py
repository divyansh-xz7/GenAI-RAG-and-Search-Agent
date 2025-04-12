import os
from schemas import schema
from services.api_service import *
from models.pydantic_models import *
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException


# get db instance
def get_db():
    db = schema.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
        
# handle api request for create user
@app.post("/create-user", response_model=User)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # create a new user
    return handleCreateUser(user=user, db=db)


# handle api request for get sessions for a user
@app.get("/fetch-sessions/{user_id}", response_model=list[ChatSession])
def fetch_sessions(user_id: int,  db: Session = Depends(get_db)):
    # fetch all sessions for a given user id
    return handleGetSessions(user_id=user_id, db=db)


# handle api request for create session
@app.post("/create-session", response_model=ChatSession)
def create_session(session: ChatSessionBase,  db: Session = Depends(get_db)):
    # create a new session
    return handleCreateSession(user_id=session.user_id, db=db)


# handle api request to get chats for a session
@app.get("/get-session-history/{session_id}", response_model=list[ChatHistory])
def get_session_history(session_id: int,  db: Session = Depends(get_db)):
    # get the chat history for a given session id
    return handleGetChatHistory(session_id=session_id, db=db)


# api to upload files
@app.post("/upload")
def upload_document(document: UploadFile = File(...)):
    # upload a document and index it as a knowledge base
    return handleUpload(document)


#api to get response from a query
@app.post("/post-query", response_model=ChatHistory)
def post_query(query: ChatHistoryBase, format:str,  db: Session = Depends(get_db)):
    # process the user query and respond with an answer
    return handleQuery(query=query, format=format, db= db)