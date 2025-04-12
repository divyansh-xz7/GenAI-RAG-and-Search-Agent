from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


connection = "postgresql://postgres:postgres@localhost:5432/fastapidb"  
collection_name = "my_docs"
embeddings = FastEmbedEmbeddings()
vectorstore = PGVector( embeddings=embeddings, collection_name=collection_name, connection=connection, use_jsonb=True)

