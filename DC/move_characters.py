from pathfinding import bfs, create_graph
from Utilities import handle_file_data as handle_file_data
from Utilities import login_sessions
import requests

def login(user, login_type):
    if login_type == 'session':
        session = login_sessions.login_with_rga_session(user)
        return session
    else:
        session = login_sessions.login(user)
        return session
def get_starting_room(session):
    response = session.get('https://sigil.outwar.com/world')
    print(response.text)

def teleport(session, room):
    url = f'https://sigil.outwar.com/world?room={room}'
    response = session.get(url)
    print(f"Teleported to room {room}")

def move_character(session, path):
    for room in range(len(path[1:])):
        payload = {'room': path[room + 1], 'lastroom': path[room]}
        response = session.get(f'https://sigil.outwar.com/ajax_changeroomb.php', params=payload)

def main():
    teleportable_rooms = [11, 1026, 4249, 26137, 25989]
    rooms = handle_file_data.read_json('../Data/rooms.json')

    login_type = input('Login type ("session" for rga session id, otherwise "login"): ')
    end_room = input('Enter room to move to: ')

    character_list = handle_file_data.read_json('../Data/Accounts/characters.json')
    for i in character_list:
        print(i['id'], i['username'], i['server'])
    print("Enter the id of the account you want to move. ")
    user = character_list[int(input())]

    print(user)
    session = login(user['login_link'], login_type)
    teleport(session, 11)
    room_map = create_graph(rooms)
    path = bfs(room_map, 11, int(end_room), teleportable_rooms)
    for i in path:
        if i in teleportable_rooms:
            teleport(session, i)
            path = path[path.index(i):]
    print("Moving...")
    move_character(session, path)
    print("Done!")

if __name__ == '__main__':
    main()
