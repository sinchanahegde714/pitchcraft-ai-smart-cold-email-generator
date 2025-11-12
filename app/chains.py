import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant"
        )

    def extract_jobs(self, page_text):
        prompt = PromptTemplate.from_template(
            """
            You are an expert job parser.  
            Extract ALL job postings from the text below.

            ### Page Text:
            {page_text}

            ### Return JSON list ONLY:
            [
              {{
                 "role": "Job Title",
                 "experience": "Years or experience info",
                 "skills": ["skill1", "skill2"],
                 "description": "Full job description text"
              }}
            ]

            If no job is found, MAKE ONE from the text.
            Your response MUST be valid JSON.
            """
        )

        chain = prompt | self.llm
        response = chain.invoke({"page_text": page_text})

        try:
            parser = JsonOutputParser()
            jobs = parser.parse(response.content)
        except Exception:
            raise OutputParserException("Could not parse job JSON.")

        return jobs if isinstance(jobs, list) else [jobs]

    def write_mail(self, job, links):
        prompt = PromptTemplate.from_template(
            """
            You are Mohan, a Business Development Executive at AtliQ.

            You must write a friendly cold email based on this job:

            {job_description}

            Include these portfolio links naturally:
            {links}

            Use DIFFERENT HUMAN NAMES each time.
            No headings. No subject line. Just the email.
            """
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "job_description": str(job),
            "links": links
        })

        return response.content
