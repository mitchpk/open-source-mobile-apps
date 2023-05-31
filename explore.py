import utils
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os_apps = utils.get_cached_os_details()
genres = {}

for a in os_apps.values():
    if a['genre'] not in genres:
        genres[a['genre']] = 1
    else:
        genres[a['genre']] += 1

pprint(genres)
print(f'Total: {len(os_apps)}')

g = pd.DataFrame(genres, index=['quantity'])
g.plot(kind='bar')
