import os
import glob

replacements = {
    'job.get_job_type_display': 'job.skills',
    'job.salary_range': 'job.salary',
    'id_salary_range': 'id_salary',
    'job.created_at': 'job.posted_on',
    'id_job_type': 'id_skills',
    'cover_letter': 'resume',
    'job_type': 'skills',
    'salary_range': 'salary'
}

for filepath in glob.glob('templates/**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
