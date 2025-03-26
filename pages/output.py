import streamlit as st
from langchain_community.llms import Ollama


st.title("📊 Interview Question Results")

st.subheader("📊 AI Feedback on Your Answers")
llm = Ollama(model="mistral")
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
✅ Correctness: Mark as ✅ (Correct) or ❌ (Incorrect) or ❌ No Answer.
----------------------------------------------------------------------------------  
🔹 Missing Key Points: Highlight any essential details the candidate missed. 
------------------------------------------------------------------------- 
📌 Improvement Suggestions: Provide guidance on how to enhance the response.  
-----------------------------------------------------------------------------------------
- If the response is incorrect, **highlight the missing information without generic advice.
--------------------------------------------------------------------------------
- If correct, confirm accuracy with ✅.  

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


    