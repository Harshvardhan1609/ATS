from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

genai.configure(api_key=st.secrets["GOOGLE_API"])


def get_gemini_response(input,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    text = ""
    for resume in uploaded_file:
        if resume!=None:
            print(resume.read())
            with resume:
                # Create a PDF file reader object
                pdf_reader = PyPDF2.PdfReader(resume)
                
                # Loop through each page of the PDF
                for page_num in range(len(pdf_reader.pages)):
                    # Extract text from the current page
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
        else:
            return "No response Recorded"
    print(text)
    return text

## Streamlit App

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resumes against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role('There are multiple resumes plz filter accordingly'). 
 Highlight the strengths and weaknesses of the applicant ('with the name of applicant  mentioned at the top') in relation to the specified job requirements job Description is:-:.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, ('There are multiple resumes plz filter accordingly')
your task is to evaluate the resumes against the provided job description. give me the percentage of match if the resumes matches
the job description. First the name of applicants then output should come as percentages and then keywords missing and last final thoughts job Description is:-:.
"""

input_prompt2 = """
You are a highly experienced career consultant with expertise in resume evaluation and job matching. Your task is to provide feedback and improvement tips based on the weaknesses identified in the resume,
('note:- There are multiple resumes plz filter accordingly and  all were in  tabular format in which mention rank of resumes and the names of the candidates also percentage matches with the job profiles strength and weakneses')
 aligning it with the job description. 
 Please share your professional evaluation and suggestions for improvement. 
 Job improvements is:-:.
"""
st.set_page_config(page_title="Garuda ATS Resume EXpert",page_icon="favicon.jpg")
# USER AUTHENTICATION
names = ["Vinod Purohit","Kalki","Prateek"]
usernames = ["vinodpurohit","kalki","prateek"]
passwords=['$2b$12$SCLTfkGL926UVSUxKDqFy.eCD6U3F95K5ufF6yobB4Acz0wo4EGf.', '$2b$12$qbbsOz5GJlhqVS0gswIk5uUc1k0GTpxeJgQQ.It73slYjCfOGy2zO', '$2b$12$rXKiHHR032FJ3VjYi4Npj.wgYit21238P7AIBYYKvIxe4r.987ePy']

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":passwords[1]
                },
            usernames[2]:{
                "name":names[2],
                "password":passwords[2]
                }        
            }
        }



#load hashed passwords

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


authenticator = stauth.Authenticate(credentials, "garudaats_system", "garuda", cookie_expiry_days=30.0)

name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status :

    current_page = 1

    # Sidebar navigation
    st.sidebar.image("garudaaihr.png",use_column_width=True)
    st.sidebar.title("GARUDA AI")
    st.sidebar.subheader(f"Welcome {name}")
    page_selection = st.sidebar.radio("Go to", ("Garuda ATS Tracking System", "Garuda Conversation","UGC Mapping","Generate Questions(Garud GenZ)"))
    uploaded_file = st.sidebar.file_uploader("Upload your resume(PDF)...",type=["pdf"], accept_multiple_files=True)
    # Page 1: Garuda ATS Tracking System
    if page_selection == "Garuda ATS Tracking System":
        st.image("garuda.jpg", use_column_width=True)
        st.title("Garuda ATS Tracking System")
        input_text=st.text_area("Job Description: ",key="input")
        
        col2, col3, col4 = st.columns(3)

        with col2:
            submit1 = st.button("Resume Summary")

        with col3:
            submit2 = st.button("Improvements Suggestions")

        with col4:
            submit3 = st.button("Percentage match")
        
        if submit1:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt1+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")

        elif submit2:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt2+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")


        elif submit3:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt3+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")

    # Page 2: Garuda Conversation
    elif page_selection == "Garuda Conversation":
        st.image("phonix.jpg", use_column_width=True)
        st.title("Garuda Conversation")
        st.write("Ask your Question from the uploaded Resume ?")
        input_prompt4 = st.text_area("")
        submit4 = st.button("Search in Resume")
        if submit4:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt4,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")

    elif  page_selection == "UGC Mapping":
            st.image("groups.jpg", use_column_width=True)
            st.title("NORMS Matching System")
            input_text = st.text_area("Job Title: ", key="input")
            
            if uploaded_file is not None:
                pdf_content = input_pdf_setup(uploaded_file)
                
                # Read the UGC PDF file
                ugc_pdf_path = "ugc.pdf"  # Replace with the actual path to the UGC PDF file
                ugc_text = ""
                with open(ugc_pdf_path, "rb") as ugc_file:
                    ugc_pdf_reader = PyPDF2.PdfReader(ugc_file)
                    for page_num in range(len(ugc_pdf_reader.pages)):
                        page = ugc_pdf_reader.pages[page_num]
                        ugc_text += page.extract_text()
                
                input_prompt4 = "You are an best HR Resume checker with aligned job profile can you please give me percentage match of job title with the norms mentioned in the rules and regulation of ugc and job title is and give response in tabular format mentioning percentage match , strengths , weaknesses and missing experience and we are also adding ugc rules and regulation from which you have to match the profile('There are multiple resumes plz filter accordingly') : "
                
                # Generate response using Gemini
                submit6 = st.button("MAP")
                if submit6:
                        response = get_gemini_response(input_prompt4 +input_text + ugc_text, pdf_content)
                        st.subheader("HR Response")
                        st.write(response)
                        with open("response.txt", "w") as file:
                            file.write(response)
                            a = response
                            download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
                

            else:
                st.write("Please upload the resume")
    elif page_selection=="Generate Questions(Garud GenZ)":

        st.image("interview.jpg", use_column_width=True)
        st.title("Garuda GenZ Interview")
        input_job=st.text_area("Job profile:" ,key="input")
        hardness=st.radio("Difficulty Level",("Low","Medium","Hard"))
        gen_bt=st.button("Generate")
        if gen_bt==True:
            if hardness=="Low":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant with answers
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)
            if hardness=="Medium":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant with an overview and in a broad way plz check how the applicant
                would perform in real world 
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)
            if hardness=="Hard":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant make sure to 
                check the analytical knowledge and deep dive into the domain also included some cutting edge techniques of the interviewer also mention answers for that questions
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)


    if uploaded_file is not None:
        st.sidebar.write("PDF Uploaded Successfully")

    authenticator.logout("Logout","sidebar")