import requests
import datetime
import re
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import numpy as np


def stack_overflow_tag_count(tag):
    url = f"https://api.stackexchange.com/2.3/tags/{tag}/info"
    params = {'site': 'stackoverflow'}
    r = requests.get(url, params=params)
    items = r.json().get('items', [])
    return items[0]['count'] if items else 0

def remotive_job_count(keyword):
    url = "https://remotive.com/api/remote-jobs"
    r = requests.get(url)
    jobs = r.json().get('jobs', [])
    pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    return sum(
        1 for job in jobs
        if pattern.search(job['title']) or pattern.search(job.get('description', ''))
    )

def github_repo_count(keyword, since_date):
    url = "https://api.github.com/search/repositories"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    query = f"{keyword} in:name,description created:>{since_date}"
    params = {'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': 100}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    count = 0
    for repo in data.get('items', []):
        text = f"{repo['name']} {repo.get('description', '')}".lower()
        if f" {keyword.lower()} " in f" {text} ":
            count += 1
    return count



def main():
    # print(f"\n🔍 Searching Reddit comments for '{KEYWORD}' over the past 30 days...\n")
    # reddit_counts = {}
    # total = 0

    # for sub in SUBREDDITS:
    #     count = get_comment_count(sub, KEYWORD, month_ago, now)
    #     reddit_counts[sub] = count
    #     total += count
    #     print(f"r/{sub:<20} : {count} comments")

    # print(f"\n🧮 Total mentions across all subreddits: {total}")
    keyword = input("Enter a technology to analyze (e.g. rust, go, vue): ").strip()
    since_date = (datetime.utcnow() - timedelta(days=30)).date()

    print("\n📊 Gathering tech trend data...\n")

    # github = github_repo_count(keyword, since_date)
    # stack = stack_overflow_tag_count(keyword)
    # jobs = remotive_job_count(keyword)

    # print(f"🔧 GitHub repos (last 30 days): {github}")
    # print(f"💬 Stack Overflow tag count: {stack}")
    # print(f"💼 Job postings with '{keyword}': {jobs}")

    print("\n📈 Generating Google Trends graph...")
    trends_data = get_google_trends(keyword)
    if trends_data is not None:
        print(trends_data)
    else:
        print("No Google Trends data available.")


if __name__ == "__main__":
    main()

# 15+ popular coding/tech subreddits
# SUBREDDITS = [
#     'programming', 'learnprogramming', 'coding', 'compsci', 'technology',
#     'cscareerquestions', 'webdev', 'gamedev',
#     'devops', 'datascience', 'MachineLearning'
# ]

# KEYWORD = "Rust"  # Change this to any tech keyword

# # Time range: last 30 days
# now = int(datetime.datetime.utcnow().timestamp())
# month_ago = now - 30 * 24 * 60 * 60

# PUSHSHIFT_COMMENT_URL = "https://api.pushshift.io/reddit/search/comment/"

# def get_comment_count(subreddit, keyword, after, before):
#     params = {
#         'subreddit': subreddit,
#         'q': keyword,
#         'after': after,
#         'before': before,
#         'size': 0,
#         'metadata': 'true'
#     }

#     try:
#         r = requests.get(PUSHSHIFT_COMMENT_URL, params=params, timeout=10)
#         r.raise_for_status()
#         return r.json().get('metadata', {}).get('total_results', 0)
#     except requests.RequestException as e:
#         print(f"Error for r/{subreddit}: {e}")
#         return 0