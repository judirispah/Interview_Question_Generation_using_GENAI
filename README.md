# 📄 AI-Powered Interview Question Generator with Automated Evaluation

## 🚀 Overview  
The **AI-Powered Interview Question Generator** is a **Streamlit-based web application** that extracts content from **PDF documents**, generates **relevant interview questions** using **LangChain and  Mistral LLM (via Bedrock)**, and evaluates **user responses** using AI. The generated questions are stored in **AWS S3**, making them accessible for further analysis. It leverages **LangChain’s Summarization (Refine Chain)** to process large text inputs efficiently before generating questions. 

This project is designed to help individuals practice interview questions by providing **AI-generated questions** and **detailed feedback on user responses** based on correctness, key points, and improvement suggestions.  

---
# 🎯 Objective  
This project aims to **automate interview question generation** from **PDF documents** using **AI**. It leverages **LangChain’s Refine Chain** for summarization and **Mistral LLM** for question generation. The system evaluates user responses and provides **AI-driven feedback**, making it a valuable tool for:  
- **Interview Preparation** 📖  
- **Educational Assessments** 🎓  
- **Corporate Training** 🏢  

# 🚀 Usefulness  
This application is beneficial for:  
✅ **Students & Job Seekers** – Helps in **preparing for technical interviews** with AI-generated questions.  
✅ **Educators & Trainers** – Enables **automated quiz generation** from course materials.  
✅ **HR & Recruiters** – Assists in **candidate screening** by evaluating answers.  
✅ **Corporate Learning Teams** – Facilitates **interactive training programs** with AI-based assessments.  
✅ **Content Creators** – Converts PDFs into **structured Q&A formats** for learning platforms.  

## 🎯 Key Features  
- ✅ **PDF Parsing & Text Extraction:** Reads and processes PDFs to extract useful content.
- ✅ **Summarization with LangChain (Refine Chain)** to condense text  
- ✅ **AI-Based Question Generation:** Uses **LangChain & Bedrock (Mistral LLM)** to create coding and conceptual questions.  
- ✅ **Interactive User Input:** Users can answer the generated questions directly within the app.  
- ✅ **Automated AI Evaluation:** The system checks the correctness of answers, identifies missing key points, and suggests improvements.  
- ✅ **Data Storage in AWS S3:** Saves generated questions for future reference and retrieval.  
- ✅ **User-Friendly UI:** Developed using **Streamlit**, making it accessible and easy to use.  

---

## 🛠 Tech Stack  

### 📌 Programming Languages & Frameworks  
- **Python** – Core programming language  
- **Streamlit** – UI development  
- **LangChain** – LLM orchestration  

### 🤖 AI Models & Processing  
- **Mistral (via bedrock)** – LLM for question generation and evaluation  
- **Amazon Bedrock** – Text embedding model for vector storage  

### ☁ Database & Cloud Storage  
- **ChromaDB** – Vector database for storing question embeddings  
- **AWS S3** – Cloud storage for saving generated questions

## 🏗 How RAG is Used in This Project?  
1️⃣ **PDF Document Parsing & Chunking** 📄  
   - The uploaded PDF is processed and split into smaller **contextual chunks** using **LangChain’s RecursiveCharacterTextSplitter**.  

2️⃣ **Vector Database for Efficient Retrieval** 🗂  
   - **ChromaDB** stores embeddings of text chunks.  
   - **Amazon Titan-Embed-Text-v1** generates vector representations for efficient similarity search.  

3️⃣ **Retrieval of Relevant Context** 🔍  
   - When generating interview questions, the system retrieves **relevant chunks** from the vector database.  
   - This ensures that questions are **contextually accurate and well-formed**.  

4️⃣ **LLM-Based Question Generation** 🤖  
   - The retrieved context is passed to **Mistral LLM** via **LangChain’s document chain**.  
   - It formulates **structured interview questions with answers** based on the retrieved information.  




# 🔍 How It Works?

## 📌 Step 1: Upload a PDF File 📂  
- The user uploads a **PDF document** containing reference material.  
- The system extracts text . 

## 📌 Step 2: Summarization with LangChain (Refine Chain) 📑  
- Large documents are **broken into smaller chunks**.  
- **Refine Chain** summarizes each chunk **iteratively**.  
- The final summary is **more readable and contextually accurate**.  

## 📌 Step 3: AI-Based Question Generation 🤖  
- **Mistral LLM via bedrock** generates interview questions.  
- Questions are formulated based on **key topics from the summary**.  
- Generated questions are stored in **AWS S3** for future retrieval.  

## 📌 Step 4: User Provides Answers ✍️  
- The **Streamlit UI** allows users to **answer the generated questions**.  

## 📌 Step 5: AI Evaluation & Feedback ✅❌  
- **User responses are compared against expected answers**.  
- Feedback is provided on:  
  - ✅ **Correctness**  
  - ❌ **Missing Key Points**  
  - 📝 **Suggestions for Improvement**
    
    ## 📦 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/judirispah/interview-question-generator.git
cd interview-question-generator

python -m venv venv

pip install -r requirements.txt

#Create a .env file in the project directory and add the following credentials:


AWS_KEY_ID=your_aws_key
AWS_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1




