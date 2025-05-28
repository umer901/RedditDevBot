import requests
import re

def remotive_job_count(keyword):
    url = "https://remotive.com/api/remote-jobs"
    r = requests.get(url)
    jobs = r.json().get('jobs', [])
    pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    return sum(
        1 for job in jobs
        if pattern.search(job['title']) or pattern.search(job.get('description', ''))
    )
