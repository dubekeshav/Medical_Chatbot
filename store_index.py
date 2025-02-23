from src.helper import load_pdf_files, split_data, download_embeddings_model, create_index
from langchain_pinecone import PineconeVectorStore
import os
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

extracted_data = load_pdf_files(data_directory='data')
data_chunks = split_data(extracted_data)
embedding_model = download_embeddings_model()

index_name = 'medicalchatbot'
create_index(index_name, 384, 'cosine')

document_search = PineconeVectorStore.from_documents(
    documents=data_chunks,
    embedding=embedding_model,
    index_name=index_name
)

# Loading the existing index
document_search = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings_model)