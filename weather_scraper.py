
from selenium import webdriver
from config import driver_location, binary_location

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

rain_keyword = """precipitation__value now-hero__next-hour-precipitation-value">"""
print(rain_keyword)
def get_weather(name: str, destinations_info: dict[str: str | int]) -> None:
    try:
        driver.get(destinations_info[name]['yr_link'])
        content = driver.page_source
        temperature_content = content[content.index(header) + len(header):]
        temperature_content = temperature_content[temperature_content.index(r"""class="temperature temperature"""):]
        temperature_content = int(temperature_content[temperature_content.index(">") + 1:temperature_content.index("<")])
        print(f"{name}: {temperature_content}")
        destinations_info[name]['temperature'] = temperature_content

        # Rain
        rain_content = content[content.index(rain_keyword) + len(rain_keyword):]
        rain_content = rain_content[:rain_content.index("<")]
        destinations_info[name]['rain'] = rain_content
        print(rain_content)
    except Exception as e:
        return


def get_total_weather(destinations_info: dict[str: str | int]) -> None:
    for name in destinations_info:
        try:
            driver.get(destinations_info[name]['yr_link'])
            content = driver.page_source
            temperature_content = content[content.index(header) + len(header):]
            temperature_content = temperature_content[temperature_content.index(r"""class="temperature temperature"""):]
            temperature_content = int(temperature_content[temperature_content.index(">") + 1:temperature_content.index("<")])
            destinations_info[name]['temperature'] = temperature_content

            # Rain
            rain_content = content[content.index(rain_keyword) + len(rain_keyword):]
            rain_content = rain_content[:rain_content.index("<")]
            destinations_info[name]['rain'] = rain_content
        except Exception as e:
            return
        