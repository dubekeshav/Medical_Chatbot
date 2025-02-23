import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Extract data from the pdf files
def load_pdf_files(data_directory):
    # Loading all the files having a .pdf extension
    print("Loading PDF files from the data directory")
    pdf_loader = DirectoryLoader(data_directory, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = pdf_loader.load()
    print(f"Total number of documents loaded: {len(documents)}")
    return documents

def split_data(extracted_data):
    print("Splitting the data into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    data_chunks = text_splitter.split_documents(extracted_data)
    print(f"Total number of chunks created: {len(data_chunks)}")
    return data_chunks

def download_embeddings_model():
    print("Downloading the embeddings model")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    print("Embeddings model downloaded successfully")
    return embeddings

def create_index(index_name, dimensions, metric, cloud_service_provider = "aws", region = "us-east-1"):
    print("Creating the index on Pinecone")
    # initialize pinecone
    pinecone_obj = Pinecone(api_key=PINECONE_API_KEY)
    
    print(f"Checking if the index {index_name} already exists")
    # Creating the index on Pinecone
    if index_name not in pinecone_obj.list_indexes().names():
        print(f"Creating the index {index_name}")
        pinecone_obj.create_index(
            name = index_name,
            dimension = dimensions,
            metric = metric,
            spec = ServerlessSpec(
                cloud=cloud_service_provider,
                region=region
            )
        )
        
    print(f"Index {index_name} created successfully")
    