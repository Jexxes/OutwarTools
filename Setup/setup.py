from Utilities import handle_file_data as handle_file_data

class User:
    current_id = 1

    def __init__(self, username, password, security_word):
        self.id = User.current_id
        User.current_id += 1
        self.username = username
        self.password = password
        self.security_word = security_word


def welcome_message():
    print("***************\n  Welcome to \n Outwar Tools!\n***************")
    print("      by\n    MadMax\n***************\n")
    print("This program will help you set up your accounts for use with the Outwar Tools program. ")
    print("Please enter your login information below. ")


def get_user_input():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    security_word = input('Enter your security word (leave blank if not applicable): ')
    return User(username, password, security_word)


def main():
    users = []
    welcome_message()

    while True:
        user = get_user_input()
        users.append(user.__dict__)

        add_more = input('Do you want to add another user? (y/n): ')
        if add_more.lower() == 'n':
            break

    handle_file_data.write_json('../Data/Accounts/logins.json', users)


if __name__ == '__main__':
    main()
