import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv   
# Load environment variables
load_dotenv()

# Configure the generative AI with API key
genai.configure(api_key='AIzaSyB_TsPAWdazOyGr1pLI9xLHXasjuqACNig')

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

def get_token_count(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.count_tokens(input_prompt)
    return "Total tokens: " + str(response.total_tokens) 

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template for querying PDF
query_prompt_template = """
You are an intelligent assistant with a deep understanding of various fields. Your task is to answer questions based on the content of a provided PDF document. Also Explain the Content Clearly in two or three lines 

PDF Content:
{text}

Question: {question}

Please provide a detailed and accurate answer.
"""

# Streamlit app
st.set_page_config(page_title="PDF Query", page_icon=":pdf:", layout="wide")
container = st.container()

container.title("Upload a PDF and ask questions about its content")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    temp = container.chat_message(message["role"]).markdown(message["content"])

# Text area for job description (JD) is removed as it's not needed for querying PDF
question = st.chat_input("Enter your question about the PDF")

with st.sidebar:
    st.title("PDF Query")
    uploaded_file = st.file_uploader("Upload Your PDF", type="pdf", help="Please upload the PDF")

if question:
    if uploaded_file is not None and question:
        text = input_pdf_text(uploaded_file)
        input_prompt = query_prompt_template.format(text=text, question=question)
        response = get_gemini_response(input_prompt)

        temp = container.chat_message("user")
        with temp:
            temp.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        tempAI = container.chat_message("ai")
        tempAI.empty()
        with tempAI:
            tempAI.markdown(get_token_count(input_prompt))
            tempAI.markdown(response)
                
        st.session_state.messages.append({"role": "ai", "content": response})
    else:
        st.error("Please upload a PDF and enter a question.")