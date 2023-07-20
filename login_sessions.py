import requests

def login(user):
    session = requests.Session()
    login_url = 'https://sigil.outwar.com/login'
    payload = {
        'login_username': user['username'],
        'login_password': user['password']
    }
    response = session.post(login_url, data=payload)
    return session if '?cmd=logout' in response.text else None

def login_with_rga_session(rga_sess_id):
    session = requests.Session()
    url = rga_sess_id
    response = session.get(url)
    return session if '?cmd=logout' in response.text else None




