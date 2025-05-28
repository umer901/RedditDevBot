import requests

def stack_overflow_tag_count(tag):
    url = f"https://api.stackexchange.com/2.3/tags/{tag}/info"
    params = {'site': 'stackoverflow'}
    r = requests.get(url, params=params)
    items = r.json().get('items', [])
    return items[0]['count'] if items else 0
