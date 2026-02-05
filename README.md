We have built an AI Resume Screener using Python and Llama3 with Ollama.
It takes in your resume and compares it to the description of the job. It will later highlight 
how many required skills are present, what critical requirements or points are missing, and how we could make it better. 
First, we extract the text from the pdf files. Upon providing the job description, AI compares
the resume text to the job description, and prints out the comparison results in the JSON format. 
It does the comparison using semantic search primarily.
