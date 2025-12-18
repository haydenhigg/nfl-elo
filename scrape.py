from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# set up data collector
def decide(a: tuple[str, bool], b: tuple[str, bool]) -> tuple[str, str, float]:
    if a[1] and not b[1]:
        return (a[0], b[0], 1)
    elif b[1] and not a[1]:
        return (a[0], b[0], 0)
    else:
        return (a[0], b[0], 0.5)

matches = []

# scrape
YEARS = [
    2024,
    2025
]
WEEKS = [
    # 2024
    [f'pre-{i}' for i in range(4)] +
    [f'reg-{i}' for i in range(19)] +
    [f'post-{i}' for i in range(6)],
    # 2025
    [f'pre-{i}' for i in range(4)] +
    [f'reg-{i}' for i in range(16)]
]

TEAM_NAME_SELECTOR = 'ul > li > div > div > div > div > div > span.display-4'
TEAM_WON_CLASS = 'text-black'

chrome_options = Options()
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

for i, year in enumerate(YEARS):
    for week in WEEKS[i]:
        print(f'fetching matches for {year} week {week}')

        driver.get(f'https://www.nfl.com/schedules/{year}/by-week/{week}')

        team_names = driver.find_elements(By.CSS_SELECTOR, TEAM_NAME_SELECTOR)
        pair = []

        for i, el in enumerate(team_names):
            pair.append((el.text, TEAM_WON_CLASS in el.get_attribute('class')))

            if len(pair) == 2:
                matches.append(decide(*pair))
                pair = []

# release web driver and write data out
driver.quit()

with open('matches20242025.json', 'w') as f:
    json.dump(matches, f)
