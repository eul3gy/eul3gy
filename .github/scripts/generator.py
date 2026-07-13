import os
import requests
import json

username = "eul3gy"
token = os.getenv("TOKEN")

categories = [
    {
        "name": "godot",
        "github_topic": "godot",
        "title": "Godot Projects",
        "icon": "./godot.svg",
    },
    
    {
        "name": "other",
        "github_topic": "other",
        "title": "Other",
        "icon": "./code.svg",
    }
]

lines = {}

for category in categories:
    lines[category["name"]] = []

params = {
    "per_page": 100,
    "page": 1,
    "sort": "updated",
    "direction": "desc"
}

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

repos_response = requests.get(f"https://api.github.com/users/{username}/repos", params=params, headers=headers)
repos_response.raise_for_status()

for repo in repos_response.json():
    if repo["private"]: continue

    name = repo["name"]
    description = repo["description"]
    topics = repo["topics"]
    url = repo["html_url"]
    #is_fork = repo["fork"]

    md = ""
    md += f"[**{name}**]({url})"
    if description: md += f" - {description}"
    
    for category in categories:
        if category["github_topic"] in topics:
            lines[category["name"]].append(md)

lists = []

for category in categories:
    cur_lines = lines[category["name"]]
    if len(cur_lines) > 0:
        cur_list = ""
        cur_list += f"""<img src="{category["icon"]}" width="24" align="left">**{category["title"]}**\n\n"""
        cur_list += "<br>".join(cur_lines)
        lists.append(cur_list)

final_md = "\n\n<br>\n\n".join(lists)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(final_md)