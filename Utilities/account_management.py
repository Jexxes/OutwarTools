import re
from bs4 import BeautifulSoup
import requests

# I am aware that this code is a bit messy at the moment.

# Account is your RGA
class Account:
    def __init__(self, user, server, user_id, session_id, server_id):
        self.user = user
        self.server = server
        self.user_id = user_id
        self.session_id = session_id
        self.server_id = server_id
        self.login_url = f"https://{server}.outwar.com/world.php?rg_sess_id={session_id}&suid={user_id}&serverid={server_id}"

# Character is each playable character on your RGA
class Character:

    def __init__(self, id, suid, server, account, username, link, login_link, level, crew_name):
        self.id = id
        self.suid = suid
        self.server = server
        self.account = account
        self.username = username
        self.link = link
        self.login_link = login_link
        self.level = level
        self.crew = crew_name

def get_accounts(user, session, server):
    server_ids = {
        "sigil": "1",
        "torax": "2",
    }

    if server in server_ids:
        server_id = server_ids[server]
        response = session.get(f'https://{server}.outwar.com/myaccount?ac_serverid={server_id}')
        match = re.search(rf'suid=(\d+)&serverid={server_id}', response.text)
        if match:
            user_id = match.group(1)
            session_id_match = re.search(r'&rg_sess_id=([a-f0-9]+)', response.text)
            session_id = session_id_match.group(1) if session_id_match else None
            return Account(user['username'], server, user_id, session_id, server_id)
    return None

def get_characters(account):
    session = requests.Session()
    account_name = account['user']
    response = session.get(account['login_url'])
    response = session.get(f"https://{account['server']}.outwar.com/myaccount.php?ac_serverid={account['server_id']}")
    if response.status_code == 200:
        print("Successfully logged in!\nFetching accounts...")
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=re.compile(
        rf"^https://{account['server']}.outwar.com/world\?suid=\d+&serverid={account['server_id']}$"))

    characters = []
    id = 0

    for link in links:
        if link.text != "PLAY!":
            id += 1
            username = link.text
            level = link.find_next("td").text or "Unknown"
            crew_name = link.find_next("td").find_next("td").text or "Unknown"
            match = re.search(r"suid=(\d+)", link["href"])
            suid = match.group(1)
            login_link = f"https://{account['server']}.outwar.com/world.php?rg_sess_id={account['session_id']}&suid={suid}&serverid={account['server_id']}"
            characters.append(Character(id, suid, account['server'], account_name, username, link["href"], login_link, level, crew_name))  # Append each character to the list
    return characters

