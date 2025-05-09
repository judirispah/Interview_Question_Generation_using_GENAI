import streamlit as st
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

st.title("📊 Interview Question Results")

st.subheader("📊 AI Feedback on Your Answers")
load_dotenv()

##load groq api
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')   

llm = ChatGroq(groq_api_key=groq_api_key,model_name="gemma2-9b-it")
     
evaluation_inputs = []
for question, user_answer in st.session_state.user_answers.items():
        
                    expected_answer = st.session_state.expected_answers[question]
                    evaluation_inputs.append(f"**Question:** {question}\n**Expected Answer:** {expected_answer}\n**User's Answer:** {user_answer}\n")

if evaluation_inputs:
        # Combine all evaluations into a single batch prompt
        batch_prompt = "\n\n".join(evaluation_inputs)
        print(batch_prompt)
        full_prompt = f"""
You are an expert interviewer evaluating multiple candidate responses.  
Your task is to assess each response based on correctness, missing key points, and improvement suggestions.  



### Evaluation Criteria:  
📌 Correctness: Mark as ✅ (Correct) or ❌ (Incorrect) or ❌ No Answer.
----------------------------------------------------------------------------------  
📌 Missing Key Points: Highlight any essential details the candidate missed. 
------------------------------------------------------------------------- 
📌 Improvement Suggestions: Provide guidance on how to enhance the response.  
-----------------------------------------------------------------------------------------
- If the response is incorrect, **highlight the missing information without generic advice.
--------------------------------------------------------------------------------
- If correct,
-📌 confirm accuracy in percentage using smiliarity.  

---

### Candidate Responses:  

{batch_prompt} 

For each question, follow this format:  

**Question:** {question} 
----------------------------------------------------------
**User Answer:** {user_answer if user_answer.strip() else "❌ No Answer Provided"}  
-----------------------------------------------------------
**Expected Answer:** {expected_answer}  

Now, provide structured and insightful feedback for each response.
"""

        # Make a **single** call to the LLM instead of multiple calls
        feedback = llm.predict(full_prompt)
        st.write(feedback)


    