
from selenium import webdriver
from tqdm import tqdm
import concurrent.futures
import pickle
import json
from time import time
import os
from destination import Destination

with open("data/destinations_info.json", "r") as file:
    destinations_info: dict[str: str | int] = json.load(file)

link = "https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/1-332197/Norge/Tr%C3%B8ndelag/Trondheim/Estenstadhytta"

# Link to how to get selenium working on linux: https://gist.github.com/siumhossain/1aa24622d8fda5053581c87ca6457638

# Setup
driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'
options = webdriver.ChromeOptions()
options.add_argument('headless') # Makes it so the window doesn't open
options.binary_location = binary_location
drivers = [webdriver.Chrome(executable_path=driver_location,options=options) for i in range(4)]
i = 0
finished = {}
time1 = 0
time2 = 0
lst = [i % 4 for i in range(len(list(destinations_info.keys())))]
print(lst)
header = r"""<div class="now-hero__next-hour-temperature-text">"""
def get_weather(name: str, id: int, i: int) -> None:
    print(f"ProcessID: {id}, name: {name}\t:\t{i}\n")
    driver = drivers[id]
    driver.get(destinations_info[name]['yr_link'])
    content = driver.page_source
    try:
        content = content[content.index(header) + len(header):]
        content = content[content.index(r"""class="temperature temperature"""):]
        content = int(content[content.index(">") + 1:content.index("<")])
        destinations_info[name]['temperature'] = content
        return content
    except Exception:
        return ""
with concurrent.futures.ProcessPoolExecutor() as executor:
    lst = executor.map(get_weather, list(destinations_info.keys()), lst, [i for i in range(len(lst))])
    for i in lst:
        print(i)
# for name in tqdm(destinations_info):
#     get_weather(name)
# for item in list(finished.values()):
#     print(len(item))

# with open("data/destinations_info.json", "w") as file:
#     json.dump(destinations_info, file, indent=4)

