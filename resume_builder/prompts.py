from jinja2 import Template

key_achievement_rephrase_prompt = Template("""
        You are an expert resume writer specializing in ATS optimization and job matching.

        JOB DESCRIPTION REQUIREMENTS:
        {{job_description_text}}

        KEY ATS KEYWORDS FROM JOB DESCRIPTION:
        {{ats_keywords_list}}

        ACHIEVEMENT TO ANALYZE:
        "{{achievement}}"

        VALIDATION CHECK:
        Before proceeding, verify that you have received:
        1. Job description requirements (above)
        2. ATS keywords list (above)
        3. Achievement bullet point (above)

        If ANY of these are missing or appear as placeholders/template variables, you MUST still proceed with the task using the information available. DO NOT explain what is missing. DO NOT ask for clarification. Simply work with what you have.

        TASK:
        1. First, identify which ATS keywords from the job description are already present in the achievement
        2. Identify which critical ATS keywords are missing but could be naturally incorporated
        3. Determine if the achievement needs modification

        DECISION CRITERIA:
        - If achievement contains 3+ relevant ATS keywords AND clearly demonstrates job-relevant impact, return it AS-IS
        - If achievement is relevant but missing critical ATS keywords or lacks clarity, rephrase it

        REPHRASING RULES:
        - Integrate missing ATS keywords naturally (technologies, methodologies, tools, skills)
        - Prioritize keywords that appear multiple times in the job description
        - Use exact keyword phrases from job description (e.g., "CI/CD pipeline" not "continuous integration")
        - Maintain technical accuracy - do NOT add technologies you didn't use
        - Emphasize quantifiable results with metrics
        - Start with strong action verbs: designed, architected, built, implemented, optimized, automated, reduced, increased, delivered

        OUTPUT REQUIREMENTS:
        - Single line, {{ word_limit_min }}-{{ word_limit_max }} words maximum
        - No bullet point symbol
        - No explanations, commentary, preambles, or meta-discussion
        - ATS-optimized with natural keyword integration
        - Clear, impactful, and truthful

        CRITICAL OUTPUT INSTRUCTION:
        Your response must ONLY contain the achievement bullet point itself. 
        DO NOT include:
        - "Rephrased achievement:"
        - "Here is the achievement:"
        - "Okay, I can help..."
        - Any explanations about missing information
        - Any requests for additional data
        - Any commentary or analysis

        WRONG OUTPUT EXAMPLES (DO NOT DO THIS):
        ❌ "Rephrased achievement: [achievement text]"
        ❌ "I cannot complete this task because..."
        ❌ "Okay, I can help analyze..."
        ❌ "The job description is missing..."

        CORRECT OUTPUT EXAMPLE:
        ✓ "Designed and deployed real-time data ingestion pipeline using Kafka and Spark on AWS, reducing latency by 70% for trading systems"

        OUTPUT:
        Return strictly only the single-line achievement bullet point. No explanations, no introductions, no bullet symbols.                                   
""")



skills_prompt_template = Template("""
        You are a resume optimization assistant. Your task is to filter and sort skills based on their relevance to a job description.

        Given the following skills in JSON format:
        {{ skills | tojson(indent=2) }}

        And the following job description:
        ---
        {{job_description}}
        ---

        Instructions:
        1. Analyze the job description to identify which skills from the provided list are relevant
        2. Remove any skills that are NOT mentioned or relevant to the job description
        3. Within each category, sort the skills by relevance (most relevant first) based on:
                - Direct mentions in the job description
                - Importance indicated in the job requirements
                - Frequency of mention
        4. Only include categories that have at least one relevant skill
        5. Maintain the exact same JSON structure as the input

        Return ONLY the filtered and sorted JSON in this exact format:
        "programming_languages": ["list of skills"],
        "data_technologies": ["list of skills"],
        "databases": ["list of skills"],
        "cloud_platforms": ["list of skills"],
        "tools_and_frameworks": ["list of skills"],
        "soft_skills": ["list of skills"]

        Do not include any explanations, markdown formatting, or additional text. Return only the raw JSON.
""")
