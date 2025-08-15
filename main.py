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
    st.title("📮 Cold Email Generator")

    Url_input = st.text_input(
        "🔗 Enter a Job Post URL:",
        value="https://careers.nike.com/department-manager-nike-dolphin-mall/job/R-67111",
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
                    st.markdown(email)

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
