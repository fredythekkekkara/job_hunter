import argparse
from resume_generator import build_resume_pipeline

def main():
    parser = argparse.ArgumentParser(description="Resume Builder Agent CLI")
    parser.add_argument('kb_dir', nargs='?', default='resume_kb',
                        help='Directory with YAML knowledge base files (default: %(default)s)')
    parser.add_argument('job_description', nargs='?', default='resume_kb/job_description.txt',
                        help='Job description text file (default: %(default)s)')
    args = parser.parse_args()

    with open(args.job_description, 'r', encoding='utf-8') as f:
        job_desc = f.read()

    print("Knowledge Base Directory:", args.kb_dir)
    print("Job Description Loaded. Length:", len(job_desc), "characters")
    print("job_desc:", job_desc)

    resume = build_resume_pipeline(args.kb_dir, job_desc)
    # md_resume = resume_to_markdown(resume)
    # print(md_resume)

if __name__ == '__main__':
    main()
