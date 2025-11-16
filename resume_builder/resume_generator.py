from typing import Optional
from resume_config import Resume, BasicInfo, Experience, Skills
from kb_loader import load_yaml_files
from rag import RAGManager
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import ast
import json
import yaml
from typing import Dict, List, Any
from prompts import key_achievement_rephrase_prompt, skills_prompt_template
from jinja2 import Template


MODEL_VERSION = "deepseek-r1:8b"
MODEL = OllamaLLM(model=MODEL_VERSION)

EXT_JOB_DESC = ""
EXT_ATS_KEYWORDS = ""
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

def extract_ats_keywords(job_description: str):
    prompt = f"""
    You are an expert recruiter skilled in identifying key hard skills, abilities, tools, and technologies (HATS keywords) required for a job.

    Given the following job description, extract and list all relevant HATS keywords in a clear, concise Python list format. Only include concrete, specific skills or tools that a candidate would need to have or use in this role.

    Job Description:
    \"\"\"
    {job_description}
    \"\"\"

    Provide the output ONLY as a valid Python list of strings.
    """


    JD_ANALYSIS_PROMPT = """Analyze the following job description and extract structured information to help tailor a resume. Return ONLY a valid JSON object with no preamble, explanation, or markdown formatting.

        Job Description:
        {job_description}

        Extract and return the following information in this exact JSON structure:

        {{{{
        "job_title": "exact job title from the posting",
        "company_name": "company name if mentioned",
        "role_summary": "brief 1-2 sentence summary of the role",
        
        "ats_keywords": {{{{
            "hard_skills": ["list of technical skills, tools, technologies"],
            "soft_skills": ["list of soft skills like leadership, communication"],
            "certifications": ["required or preferred certifications"],
            "industry_terms": ["industry-specific terminology and buzzwords"]
        }}}},
        
        "required_qualifications": [
            {{{{
            "qualification": "specific requirement",
            "weight": "critical|high|medium|low",
            "category": "education|experience|skill|certification"
            }}}}
        ],
        
        "preferred_qualifications": [
            {{{{
            "qualification": "specific preference",
            "weight": "high|medium|low",
            "category": "education|experience|skill|certification"
            }}}}
        ],
        
        "key_responsibilities": [
            {{{{
            "responsibility": "specific duty or task",
            "importance": "primary|secondary|additional",
            "skills_needed": ["related skills for this responsibility"]
            }}}}
        ],
        
        "experience_requirements": {{{{
            "years_required": "X-Y years or 'not specified'",
            "level": "entry|mid|senior|lead|executive",
            "domains": ["specific domains or industries mentioned"]
        }}}},
        
        "education_requirements": {{{{
            "degree_level": "high school|associates|bachelors|masters|phd|not specified",
            "fields_of_study": ["preferred fields"],
            "alternatives_accepted": true/false
        }}}},
        
        "technical_stack": {{{{
            "programming_languages": ["languages with frequency/importance"],
            "frameworks_libraries": ["frameworks and libraries"],
            "tools_platforms": ["development tools, platforms, software"],
            "databases": ["database technologies"],
            "cloud_services": ["AWS, Azure, GCP, etc."],
            "methodologies": ["Agile, Scrum, DevOps, etc."]
        }}}},
        
        "role_characteristics": {{{{
            "type": "individual contributor|manager|hybrid",
            "team_size": "size if managing, or 'n/a'",
            "work_mode": "remote|hybrid|onsite|not specified",
            "travel_required": "percentage or yes/no",
            "reporting_to": "position title if mentioned"
        }}}},
        
        "company_culture_indicators": [
            "values, work culture hints from the description"
        ],
        
        "action_verbs": [
            "key action verbs used in the JD (develop, lead, manage, etc.)"
        ],
        
        "measurable_outcomes": [
            "any metrics, KPIs, or measurable results mentioned"
        ],
        
        "nice_to_have": [
            "additional skills or experiences that would be beneficial"
        ],
        
        "red_flags_to_address": [
            "potential gaps or concerns a candidate should address proactively"
        ],
        
        "resume_optimization_tips": [
            "specific suggestions for tailoring resume to this job"
        ]
        }}}}

        Important: Return ONLY the JSON object. No markdown code blocks, no explanations, no additional text.
        """

    prompt = JD_ANALYSIS_PROMPT.format(job_description=job_description)

    response = ollama_generate(prompt)
    # response = "['Kubernetes', 'AWS', 'Terraform', 'OpenTofu', 'Postgres', 'CDC systems', 'Docker', 'SQL', 'Python', 'Django', 'WSGI', 'Airflow', 'Spark', 'dbt', 'Jupyter', 'Datadog', 'Grafana', 'Prometheus']"
    # For demo, just split words longer than 4 letters (replace with real LLM parsing)
    print(response)
    print("********************************************************************")
    
    try:
        result = json.loads(response)
        return result
    except json.JSONDecodeError as e:
        # Handle parsing errors
        print(f"Error parsing JSON: {e}")
        # Attempt to extract JSON from markdown blocks if present
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        raise

    response_list = ast.literal_eval(response)
    return response_list










def get_personal_info(data: Dict) -> BasicInfo:

    name = data.get('name', 'N/A')
    title = data.get('title', 'N/A')
    email = data.get('email', 'N/A')
    phone = data.get('phone', 'N/A')
    location = data.get('location', 'N/A')
    linkedin = data.get('linkedin', 'N/A')
    github = data.get('github', 'N/A')
    portfolio = data.get('portfolio', 'N/A')
    summary = data.get('summary', 'N/A')

    basic_info = BasicInfo(
        name=name,
        title=title,
        email=email,
        phone=phone,
        location=location,
        linkedin=linkedin,
        github=github,
        portfolio=portfolio,
        summary=summary
    )


    """Extract and process personal information"""
    personal_info = {
        'name': name,
        'title': title,
        'email': email,
        'phone': phone,
        'location': location,
        'linkedin': linkedin,
        'github': github,
        'portfolio': portfolio,
        'summary': summary
    }
    
    print("📋 PERSONAL INFORMATION")
    print("=" * 60)
    for key, value in personal_info.items():
        if value != 'N/A':
            print(f"{key.replace('_', ' ').title()}: {value}")
    print()
    
    return basic_info


def get_experience_info(data: Dict) -> List[Experience]:
    """Extract and process experience information"""
    experiences = data.get('experience', [])
    experience_formatted = []
    for idx, exp in enumerate(experiences, 1):
        position = exp.get('position', 'N/A')
        company = exp.get('company', 'N/A')
        location = exp.get('location', 'N/A')
        start_date = exp.get('start_date', 'N/A')
        end_date = exp.get('end_date', 'N/A')
        achievements = exp.get('achievements', [])
        achievement_formatted = []
        for achievement in achievements:
            prompt = key_achievement_rephrase_prompt.render(
                    job_description=EXT_JOB_DESC,
                    ats_keywords=EXT_ATS_KEYWORDS,
                    achievement=achievement,
                    word_limit_min=10,
                    word_limit_max=15
            )
            print('--------------- PROMPT RESPONSE---------------')
            # response = ollama_generate(prompt)
            # achievement_formatted.append(response)
            print('original achievement: ', achievement)
            # print('rephrases achievement: ', response)
            print('--------------- PROMPT RESPONSE END ---------------')
        experience_entry = Experience(
            position=position,
            company=company,
            location=location,
            start_date=start_date,
            end_date=end_date,
            achievements=achievement_formatted
        )
        experience_formatted.append(experience_entry)
    



    print("💼 WORK EXPERIENCE")
    print("=" * 60)
    for idx, exp in enumerate(experiences, 1):
        print(f"\n{idx}. {position} at {company}")
        print(f"   Location: {location}")
        print(f"   Duration: {start_date} - {end_date}")
        
        if achievements:
            print("   Key Achievements:")
            for achievement in achievements:
                print(f"   • {achievement}")
    print()
    
    return experience_formatted


def get_skills_info(data: Dict) -> Dict:
    """Extract and process skills information"""
    skills = data.get('skills', {})
    skills_json_string = json.dumps(skills, indent=2)
    print(skills_json_string)
    # prompt = skills_prompt_template.render(
    #                 job_description=EXT_JOB_DESC,
    #                 skills=skills_json_string
    #         )
    #response = ollama_generate(prompt)

    print('--------------- SKILLS PROMPT RESPONSE---------------')
    # print(prompt)
    print('--------------- SKILLS PROMPT RESPONSE END ---------------')
    
    print("🛠️  SKILLS")
    print("=" * 60)
    for category, skill_list in skills.items():
        category_name = category.replace('_', ' ').title()
        if isinstance(skill_list, list):
            print(f"\n{category_name}:")
            print(f"  {', '.join(skill_list)}")
        else:
            print(f"\n{category_name}: {skill_list}")
    print()
    
    return skills


def get_publications_info(data: Dict) -> List[Dict]:
    """Extract and process publications information"""
    publications = data.get('publications', [])
    
    print("📚 PUBLICATIONS")
    print("=" * 60)
    for idx, pub in enumerate(publications, 1):
        print(f"\n{idx}. {pub.get('title', 'N/A')}")
        print(f"   Publisher: {pub.get('publisher', 'N/A')}")
        print(f"   Date: {pub.get('date', 'N/A')}")
        print(f"   URL: {pub.get('url', 'N/A')}")
        if pub.get('summary'):
            print(f"   Summary: {pub.get('summary').strip()}")
    print()
    
    return publications


def get_certifications_info(data: Dict) -> Dict:
    """Extract and process certifications and courses"""
    certifications = data.get('certifications', [])
    courses = data.get('courses', [])
    
    print("🎓 CERTIFICATIONS & EDUCATION")
    print("=" * 60)
    
    if certifications:
        print("\nCertifications:")
        for cert in certifications:
            print(f"  • {cert.get('name', 'N/A')}")
            print(f"    Issuer: {cert.get('issuer', 'N/A')} | Date: {cert.get('date', 'N/A')}")
    
    if courses:
        print("\nCourses:")
        for course in courses:
            print(f"  • {course.get('name', 'N/A')}")
            print(f"    Platform: {course.get('platform', 'N/A')} | Completed: {course.get('completion_date', 'N/A')}")
    print()
    
    return {'certifications': certifications, 'courses': courses}


def route_yaml_data(data: Dict) -> Dict:
    """
    Route parsed YAML data to appropriate handler functions
    based on the keys present in the data
    """
    processed_data = {}
    
    # Define routing rules: key -> handler function
    routing_map = {
        'name': get_personal_info,
        'experience': get_experience_info,
        'skills': get_skills_info,
        'publications': get_publications_info,
        'certifications': get_certifications_info,
        'courses': get_certifications_info
    }
    
    # Track which handlers have been called
    called_handlers = set()
    
    # Route to appropriate handlers
    for key in data.keys():
        for route_key, handler_func in routing_map.items():
            if route_key in key.lower() and handler_func not in called_handlers:
                section_name = handler_func.__name__.replace('get_', '').replace('_info', '')
                processed_data[section_name] = handler_func(data)
                called_handlers.add(handler_func)
                break
    
    return processed_data


def parse_multi_json_string(text: str) -> Dict:
    """Parse a string containing multiple JSON objects using YAML"""
    yaml_text = text.replace('} {', '}\n---\n{')
    yaml_text = yaml_text.replace('}\n{', '}\n---\n{')
    yaml_text = yaml_text.replace('}{', '}\n---\n{')
    
    documents = list(yaml.safe_load_all(yaml_text))
    
    result = {}
    for doc in documents:
        if doc and isinstance(doc, dict):
            result.update(doc)
    
    return result














def load_my_resume_data(doc: str):


    parsed_data = parse_multi_json_string(doc)
    
    # Route to appropriate handlers
    print("\n" + "=" * 60)
    print("PROCESSING RESUME DATA")
    print("=" * 60 + "\n")
    
    processed_sections = route_yaml_data(parsed_data)
    
    print("\n" + "=" * 60)
    print("✅ Processing Complete!")
    print(f"Processed {len(processed_sections)} sections: {', '.join(processed_sections.keys())}")
    print("=" * 60)



    # try:
    #     # Convert to YAML multi-document format
    #     yaml_string = doc.replace('}\n{', '}\n---\n{').replace('} {', '}\n---\n{')

    #     # Parse all documents
    #     documents = list(yaml.safe_load_all(yaml_string))
    #     print("Loading my resume data...")
    #     # extract_personal_info(doc)
    #     # Combine
    #     result = {}
    #     for doc in documents:
    #         if doc:  # Skip None values
    #             result.update(doc)

    #     print(result)
    # except:
    #     print('Error parsing YAML documents')

def extract_personal_info(doc: str):
    try:
        # Convert to YAML multi-document format
        yaml_string = doc.replace('}\n{', '}\n---\n{').replace('} {', '}\n---\n{')

        # Parse all documents
        documents = list(yaml.safe_load_all(yaml_string))
        print('-------------JSON Object----------------')
        print(documents)
        print('-------------JSON Object END----------------')
        # class BasicInfo:
        #     name: str
        #     title: str
        #     email: str
        #     phone: str
        #     location: str
        #     linkedin: Optional[str] = None
        #     github: Optional[str] = None
        #     portfolio: Optional[str] = None
        #     summary: Optional[str] = None
    except:
        print('Error parsing JSON documents')


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

def build_resume_pipeline(kb_dir: str, job_description: str) -> Resume:
    kb_data = load_yaml_files(kb_dir)
    print("Loaded KB files:", list(kb_data.keys()))

    rag_manager = RAGManager()
    rag_manager.build_or_load(kb_data)
    relevant_docs = rag_manager.query(job_description)

    # For simplicity, just combine all relevant docs text into a single string (extend as needed)
    combined_text = " ".join(relevant_docs)
    print("-------------- Retrieved Relevant Documents ----------------")
    print(combined_text)
    print("-------------- Retrieved Relevant Documents End ----------------")

    formatted_jd = extract_ats_keywords(job_description)

    print("-------------- Extracted ATS Keywords ----------------")
    print("Extracted ATS Keywords:", formatted_jd.get('ats_keywords', {}))
    EXT_ATS_KEYWORDS = formatted_jd.get('ats_keywords', {})
    EXT_JOB_DESC = formatted_jd
    load_my_resume_data(combined_text)
    print("-------------- Extracted ATS Keywords End ----------------")

    # relevant_experience = rag_manager.fetch_relevant_experience(
    #     keywords=ats_keywords
    # )
    # print("-------------- Retrieved Relevant Experience ----------------")
    # print(relevant_experience)
    # print("-------------- Retrieved Relevant Experience End ----------------")  

    # resume = fill_resume_from_kb(kb_data, combined_text, ats_keywords)
    # return resume

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
