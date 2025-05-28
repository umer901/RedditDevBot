import requests

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
