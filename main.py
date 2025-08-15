# main.py
import streamlit as st
from portfolio import Portfolio
from chain import generate_email
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="Cold Email Generator", layout="centered")

st.title("📧 Cold Email Generator")

# Load portfolio
portfolio = Portfolio()
portfolio.load_portfolio()

job_url = st.text_input("🔗 Enter a Job Post URL:")

if st.button("🚀 Generate Email"):
    try:
        if not job_url.strip():
            st.error("Please enter a valid job post URL.")
        else:
            # Fetch and clean job description
            resp = requests.get(job_url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            job_text = " ".join(soup.stripped_strings)

            if not job_text:
                st.error("Could not extract text from job URL.")
            else:
                # Query portfolio for relevant links
                skills = ["Python", "Machine Learning"]  # Replace with skill extraction
                links = portfolio.query_links(skills)

                email = generate_email(job_text + "\n\nPortfolio Links:\n" + "\n".join(links))
                st.subheader("Generated Email")
                st.write(email)
    except Exception as e:
        st.error(f"Error: {str(e)}")
