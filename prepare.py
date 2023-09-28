import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import ImageCaptionLoader
from langchain.docstore.document import Document
import os

# Initialize ChatOpenAI model
llm = ChatOpenAI(
    temperature=0, max_tokens=1000, model_name="gpt-3.5-turbo", streaming=True
)

embeddings = OpenAIEmbeddings()

# get all files from sources into a list

folder_path = "sources"
documents = []
files = os.listdir(folder_path)

for f in files:
    full_path = os.path.join(folder_path, f)
    loader = UnstructuredFileLoader(full_path)
    loaded_documents = loader.load()
    documents.extend(loaded_documents)

# load urls

urls = ["https://www.agmo.group/about-us-2/"]
loader = UnstructuredURLLoader(urls=urls)
loaded_websites = loader.load()
documents.extend(loaded_websites)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
document_chunks = text_splitter.split_documents(documents)

Path("./chroma").mkdir(parents=True, exist_ok=True)
vectordb = Chroma.from_documents(
    document_chunks, embeddings, persist_directory="chroma"
)
