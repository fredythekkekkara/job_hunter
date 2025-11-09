from typing import Optional
from resume_config import Resume, BasicInfo, Experience, Skills
from kb_loader import load_yaml_files
from rag import RAGManager
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

MODEL_VERSION = "deepseek-r1:8b"
MODEL = OllamaLLM(model=MODEL_VERSION)
# Placeholder for Ollama LLM calls
def ollama_embed_texts(texts):
    # TODO: Replace with Ollama DeepSeek embeddings
    # Currently using fallback in RAGManager for embedding
    pass

def ollama_generate(prompt_text: str) -> str:
    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    chain = prompt_template | MODEL
    # pass a mapping (dict) as input per langchain_core ChatPromptTemplate requirements
    result = chain.invoke({"input": prompt_text})
    return str(result)

def extract_ats_keywords(job_description: str) -> list:
    prompt = f"""
    You are an expert recruiter skilled in identifying key hard skills, abilities, tools, and technologies (HATS keywords) required for a job.

    Given the following job description, extract and list all relevant HATS keywords in a clear, concise Python list format. Only include concrete, specific skills or tools that a candidate would need to have or use in this role.

    Job Description:
    \"\"\"
    {job_description}
    \"\"\"

    Provide the output ONLY as a valid Python list of strings.
    """
    response = ollama_generate(prompt)
    # For demo, just split words longer than 4 letters (replace with real LLM parsing)
    return [w.strip(",.") for w in response.split() if len(w) > 4]

# def fill_resume_from_kb(kb_data: dict, job_description: str, ats_keywords: list) -> Resume:
#     resume = Resume()

#     # BasicInfo
#     basic_info_data = kb_data.get('basic_info.yml')
#     if basic_info_data:
#         resume.basic_info = BasicInfo(**basic_info_data)

#     # Skills (filter by ATS keywords intersection)
#     skills_data = kb_data.get('skills.yml', {})
#     if skills_data:
#         all_skills = skills_data.get('technical', []) + skills_data.get('tools', []) + skills_data.get('soft_skills', [])
#         filtered_skills = [s for s in all_skills if s.lower() in [k.lower() for k in ats_keywords]]
#         # fallback: if no skills matched, add all
#         if filtered_skills:
#             resume.skills = Skills(
#                 technical=[s for s in skills_data.get('technical', []) if s in filtered_skills],
#                 tools=[s for s in skills_data.get('tools', []) if s in filtered_skills],
#                 soft_skills=[s for s in skills_data.get('soft_skills', []) if s in filtered_skills],
#             )
#         else:
#             resume.skills = Skills(**skills_data)

#     # Experience (simple filtering by job description keywords)
#     exp_data = kb_data.get('experience.yml', [])
#     if exp_data:
#         matching_experience = []
#         jd_lower = job_description.lower()
#         for exp in exp_data:
#             desc = exp.get('description', '').lower()
#             if any(kw.lower() in desc or kw.lower() in exp.get('job_title', '').lower() for kw in ats_keywords):
#                 matching_experience.append(Experience(**exp))
#         # fallback: if none matched, add all
#         resume.experience = matching_experience if matching_experience else [Experience(**exp) for exp in exp_data]

#     # Similarly, you can add other sections like education, certifications, publications etc. here

#     resume.ats_keywords = ats_keywords
#     return resume

# def build_resume_pipeline(kb_dir: str, job_description: str) -> Resume:
#     kb_data = load_yaml_files(kb_dir)
#     print("Loaded KB files:", list(kb_data.keys()))

#     rag_manager = RAGManager()
#     rag_manager.build_or_load(kb_data)
#     relevant_docs = rag_manager.query(job_description)

#     # For simplicity, just combine all relevant docs text into a single string (extend as needed)
#     combined_text = " ".join(relevant_docs)
#     print("-------------- Retrieved Relevant Documents ----------------")
#     print(combined_text)
#     print("-------------- Retrieved Relevant Documents End ----------------")

#     ats_keywords = extract_ats_keywords(job_description)

#     print("-------------- Extracted ATS Keywords ----------------")
#     print("Extracted ATS Keywords:", ats_keywords)
#     print("-------------- Extracted ATS Keywords End ----------------")

#     # resume = fill_resume_from_kb(kb_data, combined_text, ats_keywords)
#     # return resume

# def resume_to_markdown(resume: Resume) -> str:
#     lines = []
#     if resume.basic_info:
#         lines.append(f"# {resume.basic_info.name}")
#         if resume.basic_info.summary:
#             lines.append(f"\n{resume.basic_info.summary}\n")

#     if resume.skills:
#         lines.append("## Skills")
#         lines.append("**Technical:** " + ", ".join(resume.skills.technical))
#         lines.append("**Tools:** " + ", ".join(resume.skills.tools))
#         lines.append("**Soft Skills:** " + ", ".join(resume.skills.soft_skills))
#         lines.append("")

#     if resume.experience:
#         lines.append("## Experience")
#         for exp in resume.experience:
#             lines.append(f"**{exp.job_title}**, {exp.company} ({exp.start_date} - {exp.end_date or 'Present'})")
#             lines.append(exp.description)
#             lines.append("")

#     return "\n".join(lines)
