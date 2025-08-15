# Force-load newer SQLite BEFORE importing chromadb anywhere
import sys
import pysqlite3
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def email_block(email_text):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, #232526 0%, #414345 100%);
            color: #f8f8f8;
            padding: 1.2rem 1rem;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.18);
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 1.08rem;
            line-height: 1.7;
            margin-bottom: 0.5rem;
            letter-spacing: 0.01em;
            transition: background 0.3s;
        ">
        {email_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    colA, colB = st.columns(2)
    with colA:
        st.download_button(
            label="⬇️ Download as .txt",
            data=email_text,
            file_name="cold_email.txt",
            mime="text/plain",
            help="Download the generated email as a text file.",
            use_container_width=True
        )
    with colB:
        if st.button("📋 Copy Email", use_container_width=True, key=email_text[:10]):
            st.session_state['copied_email'] = email_text
            st.success("Copied to clipboard! (Select and copy manually if not auto-copied)")
            st.code(email_text, language=None)



def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📮")

    st.markdown("""
        <style>
        body { overflow-x: hidden; background: linear-gradient(120deg, #181a1b 0%, #232526 100%) !important; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stTextInput, .stButton button, .stDownloadButton button {
            border-radius: 8px !important;
            font-size: 16px !important;
        }
        .stButton button, .stDownloadButton button {
            background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(255,75,75,0.08);
        }
        .stButton button:active, .stDownloadButton button:active {
            background: #FF914D !important;
        }
        .stTextInput > div > input {
            background: #232526 !important;
            color: #f8f8f8 !important;
            border: 1.5px solid #FF914D !important;
        }
        .stTextInput label, .stTextInput span, .stTextInput div {
            color: #f8f8f8 !important;
        }
        .stMarkdown, .stSubheader, .stTitle, .stInfo, .stSidebar, .stSidebarContent {
            color: #f8f8f8 !important;
        }
        @media (max-width: 768px) {
            .stTextInput, .stButton button, .stDownloadButton button { width: 100% !important; font-size: 15px !important; }
            .block-container { padding: 0.5rem !important; }
            .stSubheader, .stTitle { font-size: 1.1rem !important; }
        }
        footer { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/new-post.png", width=80)
        st.markdown("""
        ## Cold Email Generator
        <span style='font-size:15px;color:#555;'>
        🚀 Instantly craft personalized cold emails for any job post.<br>
        � Paste a job URL, get a pro-level email, copy or download it.<br>
        <br>
        <b>Tips:</b><br>
        - Use real job posts for best results.<br>
        - Edit the email before sending.<br>
        - Try different URLs for more options.<br>
        </span>
        <hr style='margin:1rem 0;'>
        <span style='font-size:13px;color:#888;'>UI by <b>Akshay Kakade</b> & <b>Maverick Jones</b></span>
        """, unsafe_allow_html=True)

    st.title("�📮 Cold Email Generator")
    st.markdown(
        "<p style='color:gray;font-size:15px;'>Enter a job post URL and get a custom-crafted cold email with relevant portfolio links.</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        url_input = st.text_input(
            "🔗 Job Post URL:",
            value="https://careers.nike.com/department-manager-nike-dolphin-mall/job/R-67111",
            help="Paste the full job post URL here."
        )
    with col2:
        regenerate = st.button("� Regenerate", use_container_width=True)
    with col3:
        clear = st.button("🧹 Clear", use_container_width=True)

    # Session state for email output
    if 'email_results' not in st.session_state:
        st.session_state['email_results'] = []
    if 'last_url' not in st.session_state:
        st.session_state['last_url'] = ''

    def generate_email():
        with st.spinner("Scraping job post and crafting your email..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                results = []
                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_email(job, links)
                    results.append((job, email))
                st.session_state['email_results'] = results
                st.session_state['last_url'] = url_input
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Button logic
    gen_col, _ = st.columns([1,3])
    with gen_col:
        generate = st.button("🚀 Generate Email", use_container_width=True)

    if generate or regenerate or (url_input and url_input != st.session_state['last_url']):
        generate_email()
    if clear:
        st.session_state['email_results'] = []
        st.session_state['last_url'] = ''

    # Show results
    if st.session_state['email_results']:
        for job, email in st.session_state['email_results']:
            st.markdown("---")
            st.subheader(f"✉ Cold Email for: {job.get('role', 'Unknown Role')}")
            email_block(email)
    else:
        st.info("No email generated yet. Enter a job post URL and click 'Generate Email'.")

    st.markdown(
        "<p style='text-align:center; color:gray; font-size:13px; margin-top:2rem;'>"
        "Created by <b>Akshay Kakade</b> & <b>Maverick Jones</b>"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
