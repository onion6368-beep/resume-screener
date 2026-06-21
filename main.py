from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
from groq import Groq
import json
from fastapi.middleware.cors import CORSMiddleware
import os


client = Groq(api_key = os.environ.get("GROQ_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

@app.get("/")
def home():
    return {"message": "Running!"}

@app.post("/upload")
async def upload_resume(
        file: UploadFile = File(...),
        job_description: str = Form("")
    ):
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    if job_description.strip():
        prompt = f"""
        Compare this resume with the job description and analyse.
        Return ONLY valid JSON in this format:

        {{
        "name": "",
        "missing_skills": ["skill1","skill2"],
        "experience_level": "... level",
        "strengths": ["skill1","skill2"],
        "match_score": 0-100,
        "hiring_recommendation": "... Match",
        "match_summary": "one line describing the match quality",
        "summary":"one paragraph"
        }}

        Job Description:
        {job_description}

        Resume:
        {text}
        """
    else:
        prompt = f"""
        Just analyse this resume only.
        Properly analyse the resume and list strengths based on what the candidate actually has.
        Do NOT assume any field or sector.
        Based on the candidate's field and experience level, suggest skills they should add to strengthen their resume.
        Return ONLY valid JSON in this format:
        {{
        "name": "",
        "missing_skills": [],
        "experience_level": "... level",
        "strengths": ["skill1","skill2"],
        "match_score": 0-100,
        "hiring_recommendation": "Resume Analysis",
        "match_summary": "one line overview of the candidate",
        "summary":"one paragraph"
        }}

        Resume:
        {text}
        """
    try:
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [
                {
                    "role" : "user",
                    "content": prompt
                }
            ]
        )
        result = response.choices[0].message.content
        result = result.replace("```json","")
        result = result.replace("```","")
        parsed_result = json.loads(result)
        return parsed_result
    except Exception as e:
        return{
            "error" : str(e)
        }