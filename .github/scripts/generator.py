import os
import requests
import json

TOKEN = os.getenv("TOKEN")

url = "https://api.github.com/users/eul3gy/repos"

params = {
    "per_page": 100,
    "page": 1,
    "sort": "updated",
    "direction": "desc"
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

repos_response = requests.get(url, params=params, headers=headers)
repos_response.raise_for_status()

godot_lines = []
other_lines = []

for repo in repos_response.json():
    if repo["private"]: continue

    name = repo["name"]
    description = repo["description"]
    topics = repo["topics"]
    url = repo["html_url"]
    is_fork = repo["fork"]

    md = "["
    if is_fork: md += "(fork) "
    md += f"{name}]({url})"
    if description: md += f" - {description}"

    if "godot" in topics:   godot_lines.append(md)
    if "other" in topics:   other_lines.append(md)

final_md = ""

# Godot Repos

final_md += """### <img src="./godot.svg" width="24" align="left">GODOT\n#### """
if len(godot_lines) > 0:
    final_md += "<br>".join(godot_lines)
else:
    final_md += "Soon!"

# Other Repos

if len(other_lines) > 0:
    final_md += "\n\n"
    final_md += """### <img src="./code.svg" width="24" align="left">OTHER\n#### """
    final_md += "<br>".join(other_lines)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(final_md)