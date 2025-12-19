from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
ACCEPT_COOKIE_ID = 'onetrust-accept-btn-handler'
LOAD_MORE_SELECTOR = 'button.Button_button__L2wUb'
TEAM_SELECTOR = 'div.ScheduleGame_sgTeam__TEPZa'
SCORE_SELECTOR = 'div.ScheduleGame_sgScore__H8jxR'

driver = webdriver.Chrome()

print('fetching matches')

driver.get('https://www.nba.com/schedule?cal=0&pd=false&region=1')
sleep(2)

driver.find_element(By.ID, ACCEPT_COOKIE_ID).click()

# load all matches
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, LOAD_MORE_SELECTOR).click()
        sleep(1)
    except NoSuchElementException:
        break

# scrape match data
team_names = driver.find_elements(By.CSS_SELECTOR, TEAM_SELECTOR)
pair = []

for i, el in enumerate(team_names):
    try:
        team_name = el.find_element(By.CSS_SELECTOR, '*:first-child') \
            .get_attribute('data-text') \
            .upper()
        is_winner = el.find_element(By.CSS_SELECTOR, SCORE_SELECTOR) \
            .get_attribute('data-did-win') == 'true'
    except NoSuchElementException:
        needs_load_more = False
        break

    pair.append((team_name, is_winner))

    if len(pair) == 2:
        if pair[0][1] or pair[1][1]:
            matches.append(decide(*pair))

        pair = []

# release web driver and write data out
driver.quit()

with open('nba-matches2025.json', 'w') as f:
    json.dump(matches, f)
