import streamlit as st
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
import pytube
import openai

# Chat UI title
st.image(
    "https://www.agmo.group/wp-content/uploads/2021/04/Agmo-Holdings-Logo-White.png"
)
st.header("Docuwizard")
st.subheader("Chat with your data like a Master")

embeddings = OpenAIEmbeddings()

# Initialize ChatOpenAI model
llm = ChatOpenAI(
    temperature=0.3, max_tokens=1000, model_name="gpt-3.5-turbo", streaming=True
)


# Load version history from the text file
def load_version_history():
    with open("version_history.txt", "r") as file:
        return file.read()


# Sidebar section for uploading files and providing a YouTube URL
# with st.sidebar:
#     # Create an expander for the version history in the sidebar
#     with st.sidebar.expander("**Version History**", expanded=False):
#         st.write(load_version_history())

#     st.info("Not sure where to start? Let me help you.")
#     with st.spinner("Generating sample questions..."):
#         n = 10

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

vectordb = Chroma(persist_directory="chroma", embedding_function=embeddings)
vectordb.get()

# Initialize Langchain's QA Chain with the vectorstore
qa = ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever())

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your questions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Query the assistant using the latest chat history
    with st.spinner("Thinking..."):
        result = qa(
            {
                "question": prompt,
                "chat_history": [
                    (message["role"], message["content"])
                    for message in st.session_state.messages
                ],
            }
        )

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        full_response = result["answer"]
        message_placeholder.markdown(full_response + "|")

    message_placeholder.markdown(full_response)
    print(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
