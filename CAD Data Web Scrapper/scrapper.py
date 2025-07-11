import requests
import os
from urllib.parse import quote

# GitHub authentication
GITHUB_TOKEN = "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" 

headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "CAD-OCR-Scraper",
    "Authorization": f"token {GITHUB_TOKEN}"
}

query = "filename:.dxf mechanical drawing"
search_url = f"https://api.github.com/search/code?q={quote(query)}&per_page=30"

os.makedirs("cad_files_raw", exist_ok=True)

response = requests.get(search_url, headers=headers)
if response.status_code != 200:
    print("GitHub API error:", response.status_code, response.text)
    exit()

items = response.json().get("items", [])

for item in items:
    repo = item["repository"]["full_name"]
    path = item["path"]

    for branch in ["main", "master"]:
        raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
        r = requests.get(raw_url, headers=headers)
        if r.status_code == 200 and b"<html" not in r.content[:20].lower():
            filename = os.path.join("cad_files_raw", os.path.basename(path))
            with open(filename, "wb") as f:
                f.write(r.content)
            print("✅ Saved:", filename)
            break
        else:
            print(f"❌ Not found on branch '{branch}':", raw_url)
