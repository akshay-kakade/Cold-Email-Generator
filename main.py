# Force-load newer SQLite BEFORE importing chromadb anywhere
import sys
import pysqlite3
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📮")

    # ===== HEADER =====
    st.markdown(
        """
        <h1 style="text-align:center; color:#FF4B4B;">📮 Cold Email Generator</h1>
        <p style="text-align:center; font-size:1.1rem; color:gray;">
            Enter a job post URL and instantly generate a personalized cold email tailored to the role.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ===== INPUT =====
    Url_input = st.text_input(
        "🔗 Job Post URL:",
        value="https://careers.nike.com/department-manager-nike-dolphin-mall/job/R-67111",
        help="Paste the link to the job post you want to target."
    )

    if st.button("🚀 Generate Email", use_container_width=True):
        with st.spinner("Scraping job post and crafting your email..."):
            try:
                loader = WebBaseLoader([Url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()

                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_email(job, links)

                    st.markdown("---")
                    st.subheader(f"✉ Cold Email for: {job.get('role', 'Unknown Role')}")

                    # Email display with copy button
                    st.code(email, language="markdown")
                    st.button("📋 Copy Email", key=f"copy_{job.get('role', 'unknown')}", on_click=lambda txt=email: st.session_state.update({"copied_email": txt}))
                    
                    if "copied_email" in st.session_state:
                        st.success("Copied to clipboard! (Press Ctrl+V to paste)")

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # ===== FOOTER =====
    st.markdown(
        """
        <hr>
        <p style="text-align:center; color:gray; font-size:0.9rem;">
            Created by <b>Akshay Kakade</b> & <b>Maverick Jones</b> 🚀
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
