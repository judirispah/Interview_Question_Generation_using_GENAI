import os
import re
import boto3
import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables
load_dotenv()

# Initialize AWS Bedrock Client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    aws_access_key_id=os.getenv('AWS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'),
    region_name="us-east-1"
)

# Function to save generated questions to S3
def save_to_s3(s3_key, s3_bucket, content):
    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=os.getenv('AWS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'),
        region_name="us-east-1"
    )
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=content)
        print("✅ File saved to S3 successfully!")
    except Exception as e:
        print(f"❌ Error saving to S3: {e}")

# Prompt templates
summary_prompt = PromptTemplate(
    input_variables=['text'],
    template="Write a short summary of the following document:\n\n{text}"
)

question_prompt = PromptTemplate(
    input_variables=["context"],
    template="""
    You are an expert at creating questions with answers based on coding materials and documentation in any language.
    Your goal is to prepare a coder for their exams and coding tests.
    
    Based on the text below, generate **10 relevant questions**:
    
    ------------
    {context}
    ------------

     Based on the above content, generate a set of relevant questions and answers.
    Ensure that:
    - Each question is numbered (1., 2., 3., etc.) followed by answer in braces(answer) .
    - The questions thoroughly cover the key concepts from the given content.
    - The answer is enclosed in `(Answer: [answer])`
    - No extra text or formatting variations  




    ensuring they follow this strict format:

    **Format:**  
    1. [Question] (Answer: [Answer])  
    2. [Question] (Answer: [Answer])  


    Now, generate the questions :
    """
)



# Streamlit UI
st.title("📂 PDF to Interview Question Generator")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
temp_dir = "temp_pdfs"
os.makedirs(temp_dir, exist_ok=True)

# Initialize session state variables
#if "user_answers" not in st.session_state:
    #st.session_state.user_answers = {}

#if "expected_answers" not in st.session_state:
    #st.session_state.expected_answers = {}



if uploaded_file:
    st.success("✅ File uploaded successfully!")
    file_path = os.path.join(temp_dir, 'uploaded_file.pdf')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Function to process PDF and generate vector embeddings
def create_vector_embeddings():
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")
    loader = PyPDFDirectoryLoader(temp_dir)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    final_docs = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(final_docs, embeddings)
    return final_docs, vector_store

# Initialize Session State
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "expected_answers" not in st.session_state:
    st.session_state.expected_answers = {}
if "questions" not in st.session_state:
    st.session_state.questions = []

if st.button("Generate Questions"):
    with st.spinner("Processing..."):
        if uploaded_file:
            input_docs, vector_store = create_vector_embeddings()
            #llm = Ollama(model="mistral")
            llm=Bedrock(model_id="mistral.mistral-7b-instruct-v0:2",client=bedrock,
                 model_kwargs={'max_tokens':200})

            # Summarize the document
            chain = load_summarize_chain(llm, chain_type="refine", refine_prompt=summary_prompt, verbose=True)
            summary = chain.run(input_docs)

            # Generate questions
            question_answer_chain = create_stuff_documents_chain(llm, question_prompt)
            chain = create_retrieval_chain(vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1}), question_answer_chain)


            #qa = RetrievalQA.from_chain_type(
               # llm=llm,
                ##chain_type="stuff",
                #retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1}),
                #chain_type_kwargs={"prompt": question_prompt, "document_variable_name": "content"}
            #)
            
            result = chain.invoke({"input": summary})
            print(result)
            questions = result['answer']
            print(questions)
            

            st.title("✅ Questions Generated!")
            s3_key = "generated_questions.txt"
            s3_bucket = 'awsbedrockblogs3'
            save_to_s3(s3_key, s3_bucket, questions)

             # Extract questions and answers using regex
            qa_pairs = re.findall(r'\d+\.\s(.*?)\s*\(Answer:\s*(.*?)\)', questions, re.DOTALL)
            question_list = [q[0].strip() for q in qa_pairs]
            expected_answers = {q[0].strip(): q[1].strip() for q in qa_pairs}
            print(qa_pairs)

# Update session state
            st.session_state.questions = question_list
            st.session_state.expected_answers = expected_answers           



            # Split question
            #question_list = re.split(r'\n\s*\d+\.\s*', questions.strip())
            #for q in question_list: 
                    #if q.strip():
                        #question_list.append(q.strip())
            #qa1 = RetrievalQA.from_chain_type(
               # llm=llm,
                #chain_type="stuff",
                ##retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1}),
                #chain_type_kwargs={"prompt": question_prompt, "document_variable_name": "content"}
            #)            

            #for i, question in enumerate(question_list):
                #st.session_state.user_answers[question] = ""
                #expected_answers[question] = chain.invoke(f"Provide a correct answer for: {question}")

            #st.session_state.questions = question_list
            #print(st.session_state.questions)
        else:
            st.error("No PDF file uploaded!")    

# Show generated questions for user input
#print(f'expected answers: {expected_answers}')
#if expected_answers and question_list:
if st.session_state.questions:
    st.subheader("📝 Answer These Questions:")
    for i, question in enumerate(st.session_state.questions):
  

        st.session_state.user_answers[question] = st.text_area(
            f"Q{i+1}: {question}",value=st.session_state.user_answers.get(question, "")
            
             )
# Submit Button
#if expected_answers and question_list:


    if st.button("Submit Answers"):
            st.switch_page("pages/output.py")  # Redirect to output page

# Evaluate answers after submission
            st.subheader("📊 AI Feedback on Your Answers")
            llm = Ollama(model="mistral")
            evaluation_inputs = []
            for question, user_answer in st.session_state.user_answers.items():
                if user_answer.strip():
                    expected_answer = st.session_state.expected_answers[question]
                    evaluation_inputs.append(f"**Question:** {question}\n**Expected Answer:** {expected_answer}\n**User's Answer:** {user_answer}\n")

            if evaluation_inputs:
        # Combine all evaluations into a single batch prompt
                    batch_prompt = "\n\n".join(evaluation_inputs)
                    full_prompt = f"""
        You are an expert interviewer evaluating multiple candidate responses.
        For each question 

         For each question in this format:
        - question
        -user answer
        -expected answer

        - Assess correctness (with ✅ for correct and ❌ for incorrect)
        - Identify missing key points (if any)
        - Provide improvement suggestions

       
        

        Here are the responses:

        {batch_prompt}

        Provide structured feedback:
        """

        # Make a **single** call to the LLM instead of multiple calls
                    feedback = llm.predict(full_prompt)
                    st.write(feedback)


    