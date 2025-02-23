from flask import Flask, request, render_template
from src.helper import load_pdf_files, split_data, download_embeddings_model, create_index
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
# Define the query to the free hugging face model
from langchain_pinecone import PineconeVectorStore
import requests
import time
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
HUGGING_FACE_ACCESS_TOKEN = os.getenv('HUGGING_FACE_ACCESS_TOKEN')

os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['HUGGING_FACE_ACCESS_TOKEN'] = HUGGING_FACE_ACCESS_TOKEN

embeddings_model = download_embeddings_model()

index_name = 'medicalchatbot'

document_search = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings_model)

# Initializing the document search as a retriever
retriever = document_search.as_retriever(search_type='similarity', search_kwargs={'k': 3})

# Define the Free LLM Query Function
def query_free_llm(prompt):
    # Hugging Face API URL for BlenderBot
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
    bearer = f'Bearer {HUGGING_FACE_ACCESS_TOKEN}'
    HEADERS = {"Authorization": bearer}  # Add your token if required

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 503:
        print("Model is currently unavailable. Please try again later.")
        time.sleep(10)
        # return query_free_llm(prompt)
    else:
        return f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}"

# Define RAG Chain
def rag_chain(query):
    # Retrieve relevant documents from Pinecone
    relevant_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Create the final query by inserting the context into the system prompt
    final_prompt = system_prompt.format(context=context) + f"\n\n####Question: {query}#### \n\n ####Answer####" 
    # final_prompt = system_prompt.format(context=truncate_text(context, 500)) + f"\n\n####Question: {query}#### \n\n ####Answer####" 
    
    # Query the free LLM
    response = query_free_llm(final_prompt)
    print(response)
    return response

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST', 'GET'])
def ask():
    user_input = request.form['msg']
    print(rag_chain(user_input))
    response = rag_chain(user_input)[0]['generated_text'].split("####Answer####")[1]
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    