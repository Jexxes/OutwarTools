from Utilities import handle_file_data
from Utilities import login_sessions
from Utilities import account_management as am

def login(user):
    session = login_sessions.login(user)
    return session


def fetch_accounts(accounts, users):
    for user in users:
        session = login(user)
        sigil_accounts = am.get_accounts(user, session, 'sigil')
        accounts.append(sigil_accounts.__dict__)
        torax_accounts = am.get_accounts(user, session, 'torax')
        accounts.append(torax_accounts.__dict__)
    return accounts

def fetch_characters(logged_in_accounts, characters):
    for account in logged_in_accounts:
        character_list = am.get_characters(account)
        for character in character_list:
            characters.append(character.__dict__)
    return characters

def main():
    accounts = []
    characters = []
    users = handle_file_data.read_json('../Data/Accounts/logins.json')
    fetch_accounts(accounts, users)
    handle_file_data.write_json('../Data/Accounts/login_sessions.json', accounts)
    logged_in_accounts = handle_file_data.read_json('../Data/Accounts/login_sessions.json')
    fetch_characters(logged_in_accounts, characters)
    handle_file_data.write_json('../Data/Accounts/characters.json', characters)


if __name__ == '__main__':
    main()

