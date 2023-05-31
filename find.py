import csv
import requests
import re
import json
from bs4 import BeautifulSoup

url_regex = r"((http:\/\/|https:\/\/|www\.)(github|gitlab|bitbucket)\.com(\/[a-zA-Z0-9_\-\.]*)+)"

apps = []
repos = {}

with open('ai_apps.csv', 'r') as data:
    reader = csv.DictReader(data)
    for row in reader:
        apps.append(row)

for i, app in enumerate(apps):
    if i % 10 == 0:
        print(f"Status: {len(repos)} repositories for {i} apps")
    print(app['pkg_name'])
    r = requests.get(f"https://play.google.com/store/apps/details?id={app['pkg_name']}")
    if r.status_code == 200:
        parsed_html = BeautifulSoup(r.text, 'html.parser')
        for s in parsed_html.select('script'):
            s.extract()
        url = re.findall(url_regex, str(parsed_html))
        if len(url) > 0:
            repos[app['pkg_name']] = [x[0] for x in url]
            with open('repos.json', 'w') as file:
                json.dump(repos, file, indent=4)
    else:
        print('Not Google Play')

print(f"Total: {len(repos)} repositories for {len(apps)} apps")
