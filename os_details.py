import json
from google_play_scraper import app
from pprint import pprint

import utils

apps = utils.get_cached_apps()
repos = utils.get_cached_repos()

os_app_ids = [i for i in apps if i in repos]
os_apps = {}

for i in os_app_ids:
    a = app(i)
    pprint(a)
    os_apps[i] = a

with open('./os_app_details.json', 'w') as file:
    json.dump(os_apps, file, indent=4)
