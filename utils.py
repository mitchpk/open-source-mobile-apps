import csv
import json

def get_google_apps() -> list[dict[str, str]]:
    apps = []
    with open('ai_apps_google_merged.csv', 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            apps.append(row)
    return apps

def read(name: str):
    with open(f'{name}.json', 'r') as file:
        return json.load(file)

def write(name: str, value):
    with open(f'{name}.json', 'w') as file:
        return json.dump(value, file, indent=4, default=str)

def get_cached_apps() -> list[str]:
    try:
        with open('apps_async.json', 'r') as file:
            return json.load(file)
    except:
        return []

def get_cached_repos() -> dict[str, list[str]]:
    try:
        with open('repos_async.json', 'r') as file:
            return json.load(file)
    except:
        return {}

def get_cached_os_details() -> dict[str, dict]:
    try:
        with open('os_app_details.json', 'r') as file:
            return json.load(file)
    except:
        return {}

def cache_apps(apps: list[str]):
    with open('apps_async.json', 'w') as file:
        json.dump(apps, file, indent=4)

def cache_repos(repos: dict[str, list[str]]):
    with open('repos_async.json', 'w') as file:
        json.dump(repos, file, indent=4)
