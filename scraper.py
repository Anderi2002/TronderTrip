
from selenium import webdriver
from tqdm import tqdm
import concurrent.futures
import pickle
import json
import time
from destination import Destination

# Website that shows points of interest in Trondheim:
link = "https://www.trondheim.no/ut-pa-tur/"

# Link to how to get selenium working on linux: https://gist.github.com/siumhossain/1aa24622d8fda5053581c87ca6457638

# Setup
driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'
options = webdriver.ChromeOptions()
# options.add_argument('headless') # Makes it so the window doesn't open
options.binary_location = binary_location
driver = webdriver.Chrome(executable_path=driver_location,options=options)

tag_start             = r"""id="articles-container"""
tag_image             = r"""srcset="""
tag_destination_class = r"""class="article-info-header"""
tag_tags_class        = r"""class="tags-container"""
tag_tags              = r"""class="tag"""

content = driver.page_source
content = content[content.find(tag_start):]

destinations = []
"""
destinations = [{"name": <destination_name>, "image_url": <image_url>, "tags": [<tags>, ...]}, ...]
"""
destinations = []
while (index := content.find(tag_image)) != -1:
    # Finds picture
    image_content = content[index + len(tag_image) + 1:]
    image_content = image_content[:image_content.find(">")].split("\n")[-1]
    image_url = "https://www.trondheim.no" + image_content[:image_content.find(".jpg") + 4]

    # Finds start of block corresponding a destination
    index = content.find(tag_destination_class)
    content = content[index + len(tag_destination_class) + 2:]
    name = content[:content.find("<")]
    # Removes start
    content = content[content.find("<") + 5:]
    # Finds tags of destination
    tags = []
    tags_content = content[content.find(tag_tags_class) + len(tag_tags_class) + 2:content.find("</div></div>") + 6]
    while (tag_index := tags_content.find(tag_tags)) != -1:
        tags.append(tags_content[tag_index + len(tag_tags) + 2:tags_content.find("</div>")])
        tags_content = tags_content[tags_content.find("</div>") + 6:]
    destinations.append(Destination(name, image_url,tags))

with open("data/destinations.pickle", "wb") as file:
    pickle.dump(destinations, file)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(Destination.download_img, destinations)

