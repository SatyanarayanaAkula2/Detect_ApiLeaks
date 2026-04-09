import requests
import os
from dotenv import load_dotenv
import base64
import time

load_dotenv()

TOKEN = os.getenv("token")

headers = {
    "Accept": "application/vnd.github+json"
}

if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

keywords=["api_key","apikey","token","access_key","private_key","password","AKIA","sk-","ghp_","sk_live_","Bearer","BEGIN PRIVATE KEY"]
file_types=[
    "extension:py",
    "extension:js",
    "extension:json",
    "extension:env",
    "extension:txt",
]

def build_queries():
    queries = []
    for keyword in keywords:
        for file_type in file_types:
            queries.append(f"{keyword} {file_type}")
    return queries


# 🔹 Parse GitHub URL
def parse_github_url(url):
    url = url.strip().rstrip("/")
    parts = url.split("/")

    if len(parts) < 5:
        raise ValueError("Invalid GitHub URL")

    return parts[3], parts[4]


# 🔹 Global Search API
def search_public_code(max_queries=10, per_page=10):
    url = "https://api.github.com/search/code"
    queries=build_queries()
    result=[]
    seen=set()
    queries=queries[:max_queries]
    for query in queries:
        try:
            params = {
                "q": f"{query} in:file",
                "per_page": per_page,
                "sort": "indexed",
                "order": "desc"
            }
            response=requests.get(url,headers=headers,params=params,timeout=10)
            if response.status_code != 200:
                print(f"GitHub API error for query '{query}': {response.status_code}")
                continue
            if response.status_code == 403:
                print("Rate limit hit, sleeping for 60 seconds...")
                time.sleep(60)
                continue
            if response.status_code == 401:
                print("Unauthorized access - check your token")
                break
            data=response.json()
            items=data.get("items",[])  
            for item in items:
                repo=item["repository"]["full_name"]
                file_name=item["name"]
                file_url=item["html_url"]
                unique_key=f"{repo}/{file_name}"
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                result.append({
                    "repo": repo,
                    "file_name": file_name,
                    "html_url": file_url
                })
                print(f"query done: {query} - found: {file_url}")
        except requests.exceptions.RequestException as e:
            print(f"Network error for query '{query}': {e}")
            continue
        return result, None


# 🔹 Get repo files
def get_repo_files(owner, repo, path="", depth=0):
    if depth > 5:
        return [], "Max depth reached"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except:
        return [], "Network error"

    if response.status_code == 404:
        return [], "Repo not found or private"

    if response.status_code != 200:
        return [], "GitHub API error"

    data = response.json()

    if not isinstance(data, list):
        return [], "Unexpected API response"

    files = []

    for item in data:
        if item["type"] == "file":
            files.append(item["url"])
        elif item["type"] == "dir":
            sub_files, err = get_repo_files(owner, repo, item["path"], depth + 1)
            if err:
                return [], err
            files.extend(sub_files)

    return files, None


# 🔹 Get file content
def get_file_content(file_url):
    try:
        response = requests.get(file_url, headers=headers, timeout=10)
    except:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    if "content" not in data:
        return None

    try:
        return base64.b64decode(data["content"]).decode("utf-8")
    except:
        return None