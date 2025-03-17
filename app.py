#RAG
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
import boto3

from langchain.chains.summarize import load_summarize_chain

from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock



import streamlit as st
import os



def save_blog_details_s3(s3_key,s3_bucket,generate_blog):
    s3=boto3.client(service_name="s3",
                     aws_access_key_id=os.getenv('AWS_KEY_ID'),
                     aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'),
                     region_name="us-east-1")

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body =generate_blog )
        print("Code saved to s3")

    except Exception as e:
        print(e) 


bedrock=boto3.client(service_name="bedrock-runtime",
                     aws_access_key_id=os.getenv('AWS_KEY_ID'),
                     aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'),
                     region_name="us-east-1")



template="""wrtie a short summary of the follwing document,
document:{text}
"""
prompt=PromptTemplate(input_variables=['text'],template=template)


prompt_template = """
    You are an expert at creating questions based on coding materials and documentation.
    Your goal is to prepare a coder or programmer for their exam and coding tests.
    You do this by asking questions about the text below:

    ------------
    {content}
    ------------

    Create questions that will prepare the coders or programmers for their tests.
    Make sure not to lose any important information.

    Based on the above content, generate a set of relevant questions .
    Ensure that:
    - Each question is numbered (1., 2., 3., etc.).
    - The questions thoroughly cover the key concepts from the given content.

    Example format:

    1. [Question 1]
      

    2. [Question 2]
      

    Now, generate the questions :
    """
PROMPT = PromptTemplate(input_variables=["content"],
    template=prompt_template 
)

# Streamlit UI
st.title("📂 Upload a PDF to Extract Interview Question")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


# Save uploaded PDF temporarily
temp_dir = "temp_pdfs"
os.makedirs(temp_dir, exist_ok=True)

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    file_path = os.path.join(temp_dir, 'uploaded_file.pdf')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

else:
    st.info("Please upload a PDF file.")


def create_vector_embeddings():
        embeddings =BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")
        loader=PyPDFDirectoryLoader(temp_dir)
        #st.info(file_path)

        docs=loader.load()
        #st.write(f"Number of documents loaded: {len(st.session_state.docs)}")
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        final_docs=text_splitter.split_documents(docs)
        #st.session_state.index=faiss

        vectors=Chroma.from_documents(final_docs,embeddings)
        return final_docs,vectors




token_size= st.number_input("Enter the token size:", min_value=0, max_value=10000)


if st.button("Generate"):
    with st.spinner("Processing..."):
        if uploaded_file and token_size:

            input,vector=create_vector_embeddings()
            #st.write("vector database is ready")

            llm=Bedrock(model_id="mistral.mistral-7b-instruct-v0:2",client=bedrock,
                model_kwargs={'max_tokens':token_size})
            
            chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt,verbose=True)
            summary=chain.run(input)

            #st.write(type(summary))


            
            qa = RetrievalQA.from_chain_type(
                                    llm=llm,
                                    chain_type="stuff",
                                    retriever=vector.as_retriever(
                                    search_type="similarity", search_kwargs={"k": 3}
                                               ),
                                    chain_type_kwargs={"prompt": PROMPT,"document_variable_name": "content" })
            
            answer=qa({"query":summary})
            
            st.title("Question generated successfully!")
            st.write(answer['result'])
            s3_key="generated_qn.txt"
            s3_bucket='awsbedrockblogs3'
            save_blog_details_s3(s3_key,s3_bucket,answer['result'])

        else:  
            st.info("Please upload a PDF file or enter the token size")          




