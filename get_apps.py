import google_play_scraper
import utils

open_source_apps = utils.read("open_source_apps")
closed_source_apps = utils.read("closed_source_apps")

with open("open_source.csv", "r") as file:
    for app_id in file.readlines():
        id = app_id.strip()
        print(id)
        if id not in open_source_apps:
            app = google_play_scraper.app(id)
            open_source_apps[id] = app

utils.write("open_source_apps", open_source_apps)

with open("closed_source.csv", "r") as file:
    for app_id in file.readlines():
        id = app_id.strip()
        print(id)
        if id not in closed_source_apps:
            app = google_play_scraper.app(id)
            closed_source_apps[id] = app

utils.write("closed_source_apps", closed_source_apps)
