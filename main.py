from itertools import chain
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import streamlit as st

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📮")

    # Branding
    st.markdown("<h1 style='color:#1f77b4;'>📮 Cold Email Generator</h1>", unsafe_allow_html=True)
    st.markdown("Easily extract job details & generate custom cold emails from any job post.")

    col1, col2 = st.columns([2, 3])

    with col1:
        Url_input = st.text_input(
            "🔗 Enter a Job Post URL:",
            value="https://careers.nike.com/department-manager-nike-dolphin-mall/job/R-67111",
            placeholder="Paste job posting link here..."
        )
        submit_button = st.button("🚀 Generate Email", use_container_width=True)

    with col2:
        if submit_button:
            with st.spinner("Processing job post... Please wait ⏳"):
                try:
                    loader = WebBaseLoader([Url_input])
                    data = clean_text(loader.load().pop().page_content)

                    portfolio.load_portfolio()
                    jobs = llm.extract_jobs(data)

                    if not jobs:
                        st.warning("No jobs found on this page. Try another URL.")
                        return

                    for idx, job in enumerate(jobs, start=1):
                        st.subheader(f"📌 Job #{idx}: {job.get('title', 'Untitled')}")
                        st.write(f"**Company:** {job.get('company', 'Unknown')}")
                        st.write(f"**Location:** {job.get('location', 'N/A')}")
                        st.write("**Skills Required:**")
                        st.write(", ".join(job.get("skills", [])) or "No skills listed")

                        links = portfolio.query_links(job.get("skills", []))
                        if links:
                            st.markdown("**📂 Relevant Portfolio Links:**")
                            for link in links:
                                st.markdown(f"- [{link}]({link})")

                        # Generate email
                        email = llm.write_email(job, links)

                        # Email Preview - Mobile Friendly
                        with st.expander("📧 View Generated Email", expanded=True):
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: #f9f9f9;
                                    padding: 15px;
                                    border-radius: 8px;
                                    border: 1px solid #ddd;
                                    font-family: Arial, sans-serif;
                                    line-height: 1.6;
                                    white-space: pre-wrap;
                                    word-wrap: break-word;
                                    font-size: 14px;
                                    color: #333;
                                ">
                                    {email.replace('\n', '<br>')}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # Download Email
                            st.download_button(
                                label="📥 Download Email as TXT",
                                data=email,
                                file_name=f"cold_email_{idx}.txt",
                                mime="text/plain"
                            )

                            # Copy Email (JS Injection)
                            copy_script = f"""
                                <script>
                                    function copyToClipboard_{idx}() {{
                                        navigator.clipboard.writeText(`{email}`);
                                        alert("Email copied to clipboard!");
                                    }}
                                </script>
                                <button onclick="copyToClipboard_{idx}()" style="
                                    padding: 6px 12px;
                                    background-color: #1f77b4;
                                    color: white;
                                    border: none;
                                    border-radius: 5px;
                                    cursor: pointer;
                                    margin-top: 10px;
                                ">📋 Copy Email</button>
                            """
                            st.markdown(copy_script, unsafe_allow_html=True)

                except Exception as e:
                    st.error("⚠️ Could not process this URL. Please ensure it’s a valid job posting.")

    st.markdown("---")
    st.caption("Made with ❤️ using LangChain + Streamlit")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
