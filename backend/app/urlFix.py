import requests

def resolve_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        print(f"Error resolving redirect: {e}")
        return None