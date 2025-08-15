import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import requests

# Page config
st.set_page_config(page_title="Cold Email Generator", layout="wide")

st.title("📮 Cold Email Generator")
st.write("Paste a job posting URL, and get a personalized cold email instantly.")

# Create instances
chain = Chain()
portfolio = Portfolio()
portfolio.load_portfolio()

# Input
url = st.text_input("Enter Job Post URL:")

if st.button("Generate Cold Email"):
    if not url.strip():
        st.error("Please enter a URL.")
    else:
        try:
            with st.spinner("Scraping website..."):
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    st.error("Failed to retrieve page.")
                    st.stop()
                raw_text = response.text

            cleaned_text = clean_text(raw_text)

            with st.spinner("Extracting job postings..."):
                jobs = chain.extract_jobs(cleaned_text)

            if not jobs:
                st.warning("No job postings found.")
                st.stop()

            for i, job in enumerate(jobs, start=1):
                st.subheader(f"{i}. {job['role']}")
                st.write(f"**Experience:** {job['experience']}")
                st.write(f"**Skills:** {job['skills']}")
                st.write(f"**Description:** {job['description']}")

                skills = job.get("skills", "").split(",")
                links_meta = portfolio.query_links(skills)
                links = [meta["links"] for meta in links_meta[0]] if links_meta else []

                email = chain.write_email(job, links)

                st.markdown("### ✉ Cold Email")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"Error: {str(e)}")
