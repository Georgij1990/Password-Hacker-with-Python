import utilities
import itertools
import string

chunk_size = 1024
args = utilities.return_args()
ip_address = args.ip_address
port = int(args.port)

with utilities.create_socket(ip_address, port) as client_socket:
    chars = string.ascii_lowercase + string.digits
    password = None
    is_break = False
    for i in range(1, 10):
        if is_break:
            break
        for l in itertools.product(chars, repeat=i):
            password = ''.join(map(str, l))
            message = password.encode('utf-8')
            client_socket.send(message)
            response = client_socket.recv(chunk_size).decode('utf-8')
            is_success = True if response == 'Connection success!' else False
            if is_success:
                print(password)
                is_break = True
                break