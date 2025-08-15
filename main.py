# Force-load newer SQLite BEFORE importing chromadb anywhere
import sys
import pysqlite3
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

# --- Email Block Component ---
def email_block(email_text, idx):
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
        ">
        {email_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Copy button
    copy_code = f"""
    <script>
    function copyToClipboard_{idx}() {{
        navigator.clipboard.writeText(`{email_text.replace("`", "\\`")}`);
        alert("✅ Email copied to clipboard!");
    }}
    </script>
    <button onclick="copyToClipboard_{idx}()" style="
        background-color: #1f77b4;
        color: white;
        padding: 0.4rem 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 8px;
        font-size: 14px;
    ">📋 Copy Email</button>
    """
    st.markdown(copy_code, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="📥 Download Email",
        data=email_text,
        file_name=f"cold_email_{idx}.txt",
        mime="text/plain"
    )


# --- Main App ---
def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📮")

    # Custom CSS
    st.markdown("""
        <style>
        body { overflow-x: hidden; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        @media (max-width: 768px) {
            .stTextInput, .stButton button, .stDownloadButton button { width: 100% !important; }
        }
        footer { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='color:#1f77b4;'>📮 Cold Email Generator</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:gray;font-size:14px;'>Enter a job post URL and instantly get a tailored cold email with relevant portfolio links.</p>",
        unsafe_allow_html=True
    )

    # Input Card
    with st.container():
        st.markdown("""
            <div style="
                background-color: #ffffff;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                margin-bottom: 1.5rem;
            ">
            """, unsafe_allow_html=True)

        url_input = st.text_input(
            "🔗 Job Post URL:",
            value="https://careers.nike.com/department-manager-nike-dolphin-mall/job/R-67111",
        )

        generate_clicked = st.button("🚀 Generate Email", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Processing
    if generate_clicked:
        with st.spinner("Scraping job post and crafting your email..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()

                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No job details found on this page. Try another URL.")
                    return

                for idx, job in enumerate(jobs, start=1):
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_email(job, links)

                    with st.expander(f"✉ Cold Email for: {job.get('role', 'Unknown Role')}", expanded=True):
                        email_block(email, idx)

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Footer
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
