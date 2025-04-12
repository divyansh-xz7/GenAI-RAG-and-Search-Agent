from LLM.store import vectorstore
from LLM.agent import GROQ_LLM as llm

csvpath = 'keywords.csv'

def get_keywords_from_chunk(text):
    prompt = f"Instructions: You are a keyword extractor which gives few keywords which best describe the text given so that these keywords can be used to know the topics contained in text [make sure that text contains enough information about the keywords that you are giving]. Output format: There should be no sentences, only few keywords[2-5] seperated by comma. Input : {text}"
    output = llm.predict(prompt)
    return output

def get_keywords(text_chunks):
    start_chunks = text_chunks[:min(len(text_chunks), 10)]
    keywords = ''
    for chunk in start_chunks:
        keywords += get_keywords_from_chunk(chunk) +','
    
    prompt = f"Intructions :You are a keyword extractor which fine tunes the list of keywords given and returns the best and selected keywords. Output Format [STRICT] : There should be no sentences, only few keywords seperated by comma. Input : {keywords}"
    final_output = llm.predict(prompt)

    return final_output


def store_embeddings(text_chunks):
    try:
        print(len(text_chunks))
        vectorstore.add_documents(text_chunks)
        # keywords = get_keywords(text_chunks)
        # print(keywords)
        # with open(csvpath, '+a') as file:
        #     file.write(keywords+',')

        return {'message':f'document processed successfully'}
    except:
        return {'message':'something went wrong'}


def drop_tables():
    vectorstore.drop_tables()