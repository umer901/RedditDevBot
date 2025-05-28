from datetime import datetime, timedelta
from github import github_repo_count
from stackoverflow import stack_overflow_tag_count
from job import remotive_job_count
from trends import get_google_trends

def run_analysis(keyword):
    since_date = (datetime.utcnow() - timedelta(days=30)).date()

    github = github_repo_count(keyword, since_date)
    stack = stack_overflow_tag_count(keyword)
    jobs = remotive_job_count(keyword)

    print(f"GitHub: {github}, Stack: {stack}, Jobs: {jobs}")

    # if keyword != 'python' and keyword != 'javascript':
    #     _, graph_path = get_google_trends(keyword)

    return {
        "github": github,
        "stack": stack,
        "jobs": jobs
    }
# , graph_path
