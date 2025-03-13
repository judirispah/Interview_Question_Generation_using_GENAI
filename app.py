#RAG
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma

from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
import faiss

from prompt import refine_template,prompt_template


import streamlit as st
import os


# Streamlit UI
st.title("📂 Upload a PDF to Extract Interview Question")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


# Save uploaded PDF temporarily
temp_dir = "temp_pdfs"
os.makedirs(temp_dir, exist_ok=True)

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

else:
    st.info("Please upload a PDF file.")


def create_vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.embeddings =OllamaEmbeddings(model='mxbai-embed-large')
        st.session_state.loader=PyPDFDirectoryLoader(temp_dir)
        st.info(file_path)

        st.session_state.docs=st.session_state.loader.load()
        #st.write(f"Number of documents loaded: {len(st.session_state.docs)}")
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        st.session_state.final_docs=st.session_state.text_splitter.split_documents(st.session_state.docs)
        #st.session_state.index=faiss

        st.session_state.vectors=Chroma.from_documents(st.session_state.final_docs,st.session_state.embeddings)
        st.session_state.save

if st.button("Generate"):
    if uploaded_file:
        create_vector_embeddings()
        st.write("vector database is ready")
    else:  
        st.info("Please upload a PDF file.")          




