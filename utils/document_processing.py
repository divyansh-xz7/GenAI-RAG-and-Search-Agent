from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPowerPointLoader
import pandas as pd

# Split on spaces, periods, and newlines 
text_splitter = RecursiveCharacterTextSplitter(separators=[" ", ".", "\n"], chunk_size=1000, chunk_overlap=20, length_function=len, is_separator_regex=False,) 

#load and split documents
def loadAndSplitDoc(file, file_type, encoding):
    print(file_type)
    if file_type == 'application/pdf':

        # print(f'Loading file}')
        loader = PyPDFLoader (file)
        text = loader.load()
        documents = text_splitter.split_documents(text)
        return documents

    elif file_type=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        loader = Docx2txtLoader(file)
        text = loader.load()
        documents = text_splitter.split_documents(text)
        return documents


    elif file_type == 'application/vnd.ms-excel':
        loader = UnstructuredExcelLoader(file)
        text = loader.load()
        documents = text_splitter.split_documents(text)
        return documents
    
    elif file_type == 'text/csv':
        print("under csv")
        table = pd.read_csv(file, encoding=encoding)
        table = table.astype(str)
        text = ' '.join(table.values.flatten())
        chunks = text_splitter.split_text(text)
        docs = [Document(text) for text in chunks]
        return docs
    
    elif file_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
        loader = UnstructuredPowerPointLoader(file)
        text = loader.load()
        documents = text_splitter.split_documents(text)
        return documents

     
    else :
        print(file_type)
        return None
    