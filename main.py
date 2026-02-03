#convert the pdf files into raw text so LLMs  
#can read them using PyaMuPDF

import fitz
import ollama
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def screen_resume(resume_text, job_description):
    prompt = f"""
    You are a Senior Technical Recruiter with 20 years of experience.
    Your goal is to objectively evaluate a candidate based on a Job Description (JD).

    JOB DESCRIPTION:
    {job_description}

    CANDIDATE RESUME:
    {resume_text}

    TASK:
    Analyze the resume against the JD. Look for key skills, experience
    levels, and project relevance. 
    Be script but fair. "React" matches "React.js". "AWS" matches "Amazon Web Services".

    OUTPUT FORMAT:
    Provide the response in valid JSON format only. Do not add any conversational text.
    structure:
    {{
        "candidate_name": "extracted name",
        "match_score": "0-100",
        "key_strengths": ["list of 3 key strengths"],
        "missing_critical_skills": ["list of missing skills"],
        "recommendation": "Interview" or "Reject",
        "reasoning": "A 2-sentence summary of why."
    }}
    """
    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])

    return response['message']['content']

job_description = """
We are looking for a Junior Data Scientist.
Must have:
- Python (Pandas, NumPy, Scikit-Learn)
- Experience with SQL
- Basic understanding of Machine Learning algorithms
- Good communication skills
Nice to have:
- Experience with AWS or Cloud deployment
- Knowledge of NLP
"""

try:
    resume_text = extract_text_from_pdf("/Users/chikus/Documents/resume_shrutim_pdf.pdf")
except Exception as e:
    print(f"Error loading resume: {e}")
    exit()

print("AI is analyzing the candidate... (this may take a few seconds on local hardware)")
result_json_string = screen_resume(resume_text, job_description)

try:
    clean_json = result_json_string.replace("```json", "").replace("```", "").strip()
    result_data = json.loads(clean_json)

    print("\n--- SCREENING REPORT ---")
    print(f"Candidate: {result_data.get('candidate_name', 'Unknown')}")
    print(f"Score: {result_data.get('match_score')}/100")
    print(f"Decision: {result_data.get('recommendation').upper()}")
    print(f"Missing Skills: {', '.join(result_data.get('missing_critical_skills', []))}")
    print(f"Reasoning: {result_data.get('reasoning', 'No reasoning provided.')}")
except json.JSONDecodeError:
    print("Failed to parse JSON. Raw output:")
    print(result_json_string)