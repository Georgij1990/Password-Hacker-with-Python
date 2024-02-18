import json
import utilities
import itertools

chunk_size = 1024
args = utilities.return_args()
ip_address = args.ip_address
port = int(args.port)
with utilities.create_socket(ip_address, port) as client_socket:
    correct_login = utilities.find_login(client_socket, chunk_size)
    correct_dict = utilities.find_password(client_socket, chunk_size, correct_login)
print(json.dumps(correct_dict))

