import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import ImageCaptionLoader
from langchain.docstore.document import Document
import os

os.environ["OPENAI_API_KEY"] = "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"

# Initialize ChatOpenAI model
llm = ChatOpenAI(
    temperature=0, max_tokens=1000, model_name="gpt-3.5-turbo", streaming=True
)

embeddings = OpenAIEmbeddings()

documents = []
loader = UnstructuredFileLoader("agmo2023.pdf")
loaded_documents = loader.load()
documents.extend(loaded_documents)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
document_chunks = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(
    document_chunks, embeddings, persist_directory="chroma"
)
