# reads ai_apps.csv and outputs ai_apps_google.csv, including only google play apps

import csv
import aiohttp
import asyncio
import utils

apps: list[dict[str, str]] = []
with open('ai_apps.csv', 'r') as data:
    reader = csv.DictReader(data)
    for row in reader:
        apps.append(row)

prevApps = utils.get_cached_apps()

async def main():
    timeout = aiohttp.ClientTimeout(
        total=None, # default value is 5 minutes, set to `None` for unlimited timeout
        sock_read=30,
        sock_connect=30,
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        results: list[int] = [i for i in await asyncio.gather(
                    *[get(id, session) for id in range(len(apps)) if apps[id]['pkg_name'] not in prevApps])
                  if i is not None]

    with open('ai_apps_google.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['sha256', 'pkg_name'])
        rows = [apps[i] for i in results]
        rows.extend([i for i in apps if i['pkg_name'] in prevApps])
        writer.writeheader()
        writer.writerows(rows)

async def get(id, session: aiohttp.ClientSession):
    name = apps[id]['pkg_name']
    try:
        async with session.get(url=f"https://play.google.com/store/apps/details?id={name}") as response:
            if response.status != 200:
                print(f"{name} is not Google Play")
                return

            print(f"Successfully got {name}")

            return id

    except Exception as e:
        print(f"Unable to get {name} due to {e.__class__}")

asyncio.run(main())
