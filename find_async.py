import aiohttp
import asyncio
import re
import utils
from bs4 import BeautifulSoup

url_regex = r"((http:\/\/|https:\/\/|www\.)(github|gitlab|bitbucket)\.com(\/[a-zA-Z0-9_\-\.]*)+)"

apps = utils.get_google_apps()
prevApps = utils.get_cached_apps()
prevRepos = utils.get_cached_repos()

apps = list(filter(lambda x: x['pkg_name'] not in prevApps, apps))

async def main():
    timeout = aiohttp.ClientTimeout(
        total=None, # default value is 5 minutes, set to `None` for unlimited timeout
        sock_read=30,
        sock_connect=30,
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = [i for i in await asyncio.gather(
                    *[get(id, session) for id in range(len(apps))])
                  if i is not None]

    repos = [i for i in results if len(i[1]) > 0]
    # most recent: 344 repositories for 31401 apps
    print(f"Found {len(repos)} more repos for {len(results)} more apps")
    print(f"Total: {len(repos) + len(prevRepos)} repositories for {len(results) + len(prevApps)} apps")

    # save results
    data = [i[0] for i in results]
    data.extend(prevApps)
    utils.cache_apps(data)
    utils.cache_repos(dict(repos) | prevRepos)

async def get(id, session: aiohttp.ClientSession):
    name = apps[id]['pkg_name']
    try:
        async with session.get(url=f"https://play.google.com/store/apps/details?id={name}") as response:
            if response.status != 200:
                print(f"{name} is not Google Play")
                return

            print(f"Successfully got {name}")
            resp = await response.text()

            parsed_html = BeautifulSoup(resp, 'html.parser')
            for s in parsed_html.select('script'):
                s.extract()
            url: list[tuple[str]] = re.findall(url_regex, str(parsed_html))
            return name, [x[0] for x in filter(lambda x: "privacy" not in x[0].lower(), url)]

    except Exception as e:
        print(f"Unable to get {name} due to {e.__class__}")

asyncio.run(main())
