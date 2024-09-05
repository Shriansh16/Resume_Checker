import streamlit as st
import PyPDF2 as pdf
from openai import OpenAI
client = OpenAI(st.secrets["api_key"])
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": input}] ,
    max_tokens=150,
    n=1
    )
    
    return response.choices[0].message.content
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt_template = """
You are a highly specialized Application Tracking System (ATS) focused solely on evaluating IT resumes. Analyze the candidate's resume based on the provided job description and return only the following information:

1. "Matching Score" as a percentage of how well the resume fits the job description.
2. "Relevance Score" as a percentage of how relevant the candidate’s experience and skills are for the role.
3. The most suitable IT department for the interview (e.g., AI/ML department, Software Development, Cybersecurity, Data Science, etc.).

resume: {text}
job description: {jd}

Return the response in exactly this format, with no extra text or explanations:
"Matching Score": "<value>%"\n
"Relevance Score": "<value>%"\n
"Department for interview": "<department name>"
"""

## streamlit app
st.title("Resume Match Analyzer")
jd = st.text_area("Paste the Job Description")  
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(text=resume_text, jd=jd)
        response = get_response(input_prompt)
        st.write(response)