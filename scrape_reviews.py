import google_play_scraper as gp
import utils
import multiprocessing

def get_reviews(app):
    print(app)
    result, _ = gp.reviews(app, count=100000)
    print(app, "finished")
    return app, result

if __name__ == "__main__":
    os_apps = utils.read("open_source_apps")
    cs_apps = utils.read("closed_source_apps")
    reviews = utils.read("reviews")

    multiprocessing.set_start_method("spawn")
    apps = list(os_apps.keys()) + list(cs_apps.keys())
    filtered_apps = []
    for app in apps:
        if app not in reviews:
            filtered_apps.append(app)

    with multiprocessing.Pool(len(filtered_apps)) as pool:
        for app, result in pool.map(get_reviews, filtered_apps):
            reviews[app] = result

    utils.write("reviews", reviews)
