
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import extract_job_post_content
import datetime
import requests

st.set_page_config(
    page_title="Cold Email Generator Pro",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    .stButton>button {
        background-color: #0072ff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 2em;
        margin: 0.5em 0;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #0059b3;
        color: #fff;
    }
    .stTextArea textarea {
        border-radius: 8px;
        min-height: 200px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📧 Cold Email Generator Pro")
st.write("Generate, copy, and download professional cold emails in seconds.")

with st.form("email_form"):
    job_post_link = st.text_input("Paste Job Post Link (optional)", "")
    recipient = st.text_input("Recipient Name", "John Doe")
    company = st.text_input("Company Name", "Acme Corp")
    product = st.text_input("Your Product/Service", "AI-powered CRM")
    pain_point = st.text_input("Pain Point", "manual data entry")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Persuasive", "Casual"])
    custom_message = st.text_area("Custom Message (optional)", "")
    submit = st.form_submit_button("Generate Email 🚀")

if submit:
    job_post_content = ""
    if job_post_link.strip():
        try:
            job_post_content = extract_job_post_content(job_post_link)
        except Exception as e:
            st.warning(f"Could not fetch job post: {e}")
    # Use Chain and Portfolio to generate the email using AI prompt and relevant links
    chain = Chain()
    portfolio = Portfolio()
    portfolio.load_portfolio()
    # Compose a job description from the form fields and job post content
    job = {
        "role": recipient,
        "experience": "",
        "skills": product,
        "description": f"Company: {company}\nPain Point: {pain_point}\nCustom Message: {custom_message}\nJob Post: {job_post_content}"
    }
    # Query relevant links from portfolio using product/skills
    links = portfolio.query_links(product)
    email = chain.write_email(job, links)
    st.session_state["generated_email"] = email
    st.session_state["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if "generated_email" in st.session_state:
    st.subheader("Generated Email")
    st.text_area("Email", st.session_state["generated_email"], height=600, key="email_output")
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        st.download_button(
            label="Download as .txt",
            data=st.session_state["generated_email"],
            file_name=f"cold_email_{st.session_state['timestamp'].replace(':','-')}.txt",
            mime="text/plain"
        )
    with col2:
        st.button("Copy Email", on_click=lambda: st.write("Copied! (Use your mouse/keyboard)") )
    with col3:
        st.button("Generate Another Email", on_click=lambda: st.session_state.pop("generated_email"))

    st.markdown("---")
    st.markdown("**Pro Features:**")
    st.markdown("- Save email history")
    st.markdown("- Use templates")
    st.markdown("- Preview in mobile/desktop mode")
    st.markdown("- Share via email directly (coming soon)")
    st.markdown("- More AI-powered suggestions")

st.sidebar.header("About")
st.sidebar.info("""
This is a professional cold email generator app built with Streamlit. 

- Generate high-converting emails
- Copy or download instantly
- Beautiful, modern UI

Made by a pro, for pros.
""")
