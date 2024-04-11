from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2

genai.configure(api_key=st.secrets["GOOGLE_API"])
# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
    <img src="garuda.jpg" alt="Banner Image">
</div>
<style>
    .banner {
        width: 160%;
        height: 200px;
        overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""
# Display the custom HTML



def get_gemini_response(input,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file!=None:
        print(uploaded_file.read())
        text = ""
        with uploaded_file:
            # Create a PDF file reader object
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            # Loop through each page of the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extract text from the current page
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        print(text)
        return text
    else:
        return "No response Recorded"

## Streamlit App

st.set_page_config(page_title="Garuda ATS Resume EXpert")
st.components.v1.html(custom_html)
st.header("Garuda ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Give Suggestions for Improvements")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements job Description is:-:.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts job Description is:-:.
"""

input_prompt2 = """
You are a highly experienced career consultant with expertise in resume evaluation and job matching. Your task is to provide feedback and improvement tips based on the weaknesses identified in the resume, aligning it with the job description. Please share your professional evaluation and suggestions for improvement. Job improvements is:-:.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1+input_text,pdf_content)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2+input_text,pdf_content)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3+input_text,pdf_content)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please upload the resume")
