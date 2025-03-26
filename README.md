# Interview_Question_Generation_using_GENAI

📄 AI-Powered Interview Question Generator with Automated Evaluation
🚀 Overview
The AI-Powered Interview Question Generator is a Streamlit-based web application that extracts content from PDF documents, generates relevant interview questions using LangChain and Mistral LLM (via Ollama), and evaluates user responses using AI. The generated questions are stored in AWS S3, making them accessible for further analysis.

This project is designed to help individuals practice interview questions by providing AI-generated questions and detailed feedback on user responses based on correctness, key points, and improvement suggestions.

🎯 Key Features
✅ PDF Parsing & Text Extraction: Reads and processes PDFs to extract useful content.
✅ AI-Based Question Generation: Uses LangChain & Ollama (Mistral LLM) to create coding and conceptual questions.
✅ Interactive User Input: Users can answer the generated questions directly within the app.
✅ Automated AI Evaluation: The system checks the correctness of answers, identifies missing key points, and suggests improvements.
✅ Data Storage in AWS S3: Saves generated questions for future reference and retrieval.
✅ Secure & Scalable: Uses Amazon Bedrock for embeddings, ensuring efficient text processing.
✅ User-Friendly UI: Developed using Streamlit, making it accessible and easy to use.

🛠 Tech Stack
Programming Languages & Frameworks:
Python – Core programming language

Streamlit – UI development

LangChain – LLM orchestration

FastAPI (Optional) – For backend API (future enhancement)

AI Models & Processing:
Mistral (via Ollama) – LLM for question generation and evaluation

Amazon Bedrock – Text embedding model for vector storage

Database & Cloud Storage:
ChromaDB – Vector database for storing question embeddings

AWS S3 – Cloud storage for saving generated questions

Tools & Services:
Docker – Containerization for deployment

GitHub Actions – CI/CD automation

MLflow – Model tracking (planned feature)

dotenv – For managing environment variables

📦 Installation & Setup
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/interview-question-generator.git
cd interview-question-generator
2️⃣ Create a Virtual Environment & Activate It
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file in the project directory and add the following credentials:

plaintext
Copy
Edit
AWS_KEY_ID=your_aws_key
AWS_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
MODEL_ID=amazon.titan-embed-text-v1
OLLAMA_MODEL=mistral
5️⃣ Run the Application
bash
Copy
Edit
streamlit run app.py
📸 Screenshots & Demo
(Add relevant screenshots or a demo link here to showcase the UI & functionality.)

📊 How It Works?
Step 1: Upload a PDF File 📂
The system extracts text from the uploaded PDF.

The text is processed and converted into vector embeddings using Amazon Bedrock.

Step 2: AI Generates Interview Questions 🤖
The extracted text is fed into the Mistral LLM via LangChain, which generates relevant interview questions with answers.

The generated questions follow a structured format.

Step 3: User Inputs Answers ✍️
Users attempt the questions by typing their responses in the provided input fields.

Step 4: AI Evaluation & Feedback ✅❌
The system compares user answers with expected answers.

AI evaluates correctness and identifies missing key points.

Improvement suggestions are provided to enhance the user’s responses.

Step 5: Save Questions & Answers to AWS S3 ☁
The generated questions and answers are stored in AWS S3 for future use.
