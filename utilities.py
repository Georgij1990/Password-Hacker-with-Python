import argparse
import socket


def return_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port')
    # parser.add_argument('message')
    args = parser.parse_args()
    return args


def create_socket(ip, port):
    client_socket = socket.socket()
    client_socket.connect((ip, port))
    return client_socket