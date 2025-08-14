import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import streamlit as st

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=st.secrets["GROQ_API_KEY"],  model_name="llama-3.1-8b-instant")


    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Failed to extract job postings")
        return res if isinstance(res, list) else [res]

    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are Mandy Jones, a Business Development Executive at Amber. Amber is an AI & Software company that focuses on the seamless integration of business processes through automated tools.
        Over our experience, we have empowered numerous enterprises with tailored solutions leading to process optimization, cost reduction, and heightened overall efficiency.
        Your job is to write a cold email to the client regarding the job mentioned above and assist them in fulfilling their needs.
        Also, add the most relevant ones from the following links to showcase AtliQ's portfolio: {link_list}
        Remember: You are Mandy Jones, BDE at Amber.
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):

        """)

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
