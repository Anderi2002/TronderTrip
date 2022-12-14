
from selenium import webdriver
from tqdm import tqdm
import concurrent.futures
import pickle
import json
import time
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
driver = webdriver.Chrome(executable_path=driver_location,options=options)

header = r"""<div class="now-hero__next-hour-temperature-text">"""
def get_weather(name:str) -> None:
    try:
        driver.get(destinations_info[name]['yr_link'])
        content = driver.page_source
        content = content[content.index(header) + len(header):]
        content = content[content.index(r"""class="temperature temperature"""):]
        content = int(content[content.index(">") + 1:content.index("<")])
        print(f"{name}: {content}")
        destinations_info[name]['temperature'] = content
    except Exception as e:
        return

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(get_weather, list(destinations_info.keys()))
for name in destinations_info:
    get_weather(name)

with open("data/destinations_info.json", "w") as file:
    json.dump(destinations_info, file, indent=4)
