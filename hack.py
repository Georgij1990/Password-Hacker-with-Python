import json
import socket
import utilities

chunk_size = 1024
args = utilities.return_args()
ip_address = args.ip_address
port = int(args.port)
with socket.socket() as client_socket:
    client_socket.connect((ip_address, port))
    correct_login = utilities.find_login(client_socket, chunk_size, 'logins.txt')
print(json.dumps(correct_login))

