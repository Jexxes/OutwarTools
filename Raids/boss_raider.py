import json
import requests
import re
from bs4 import BeautifulSoup
import datetime
import time
from Utilities import handle_file_data


def login(account):
    session = requests.Session()
    login_url = account['login_url']
    response = session.get(login_url)
    return session if '?cmd=logout' in response.text else None

def get_available_bosses(account, session):
    url = f"https://{account['server']}.outwar.com/crew_bossspawns"
    response = session.get(url)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')

    boss_cards = soup.find_all("div", class_="card-body p-2")

    for card in boss_cards:
        boss_name = card.find("h3", class_="card-user_name").text.strip()
        life_left_element = card.find("p", class_="card-user_occupation")

        if life_left_element:
            life_left_text = life_left_element.text.strip().split()
            if life_left_text:
                life_left = life_left_text[0]
            else:
                life_left = "0%"
        else:
            life_left = "0%"

        print(f"Boss: {boss_name}")
        print(f"Life Left: {life_left}")
        print()



def check_failed_raid(response):
    pattern = r'You need (\d+) rage'

    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        return "Not enough Rage"
    pattern = r'There must be at least (\d+) people in this raid'
    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        return "Not enough people in raid"
    return None

def join_raid(session, user, raid_link):
    url = user['link']
    response = session.get(url)
    url = raid_link
    response = session.get(url)
    payload = {
        'submit': 'Join This Raid!',
        'submit': 'Join This Raid!',
        'join': '1'
    }
    response = session.post(url, data=payload)
    if response.status_code == 200:
        print("Successfully joined the raid!")
    else:
        print("Failed to join the raid!")

def form_raid(user, server, session):
    url = user['link']
    response = session.get(url)
    url = f"https://{server}.outwar.com/formraid.php?target=127"
    response = session.get(url)
    JoinPayload = {
        'formtime': '1',
        'submit': 'Join This Raid!',
        'submit': 'Join This Raid!'}
    response = session.post(url, data=JoinPayload)
    url = response.url
    if "joinraid.php?raidid=" in url:
        print("Successfully formed the raid!")
        return url
    else:
        print("Failed to form the raid!")
        check_failed_raid(url.text)
        return None

def launch_raid(session, user, raid_link):
    url = user['link']
    response = session.get(url)
    url = raid_link + '&launchraid=yes'
    response = session.get(url)
    url = response.url
    response = session.get(url)
    print("Successfully launched the raid!")
    return True


def main():
    starting_time = datetime.datetime.now()
    next_hour = starting_time.hour + 1
    raiding_crew = input("Raiding crew name: ")
    server = input("Server: ")
    while True:
        accounts = handle_file_data.read_json('../Data/Accounts/login_sessions.json')
        users = handle_file_data.read_json('../Data/Accounts/characters.json')
        for account in accounts[:1]:
            session = login(account)
            if session:
                get_available_bosses(account, session)
                former_saved = False
                for user in users:
                    if not former_saved:
                        former = user
                        raid_link = form_raid(user, server, session)
                        former_saved = True
                    if user['crew'] == raiding_crew and former:
                        join_raid(session, user, raid_link)
        launched = launch_raid(session, former, raid_link)
        if launched:
            launch_time = datetime.datetime.now()
            print(f"Raid launched at {launch_time}")
            seconds_until_next_minute = 65 - launch_time.second
            print(f"Next raid in {seconds_until_next_minute} seconds")
            time.sleep(seconds_until_next_minute)


if __name__ == "__main__":
    main()