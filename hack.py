import utilities
import itertools

chunk_size = 1024
args = utilities.return_args()
ip_address = args.ip_address
port = int(args.port)

with utilities.create_socket(ip_address, port) as client_socket:
    is_break = False
    previous_word = ''
    for row in utilities.read_file('passwords.txt'):
        typical_pass = row.rstrip('\n')
        combinations = [''.join(chars) for chars in itertools.product(*[(c.lower(), c.upper()) for c in typical_pass])]
        for psswrd in combinations:
            message = psswrd.encode('utf-8')
            try:
                client_socket.send(message)
                response = client_socket.recv(chunk_size).decode('utf-8')
            except:
                pass
            is_success = True if response == 'Connection success!' else False
            if is_success:
                print(psswrd)
                is_break = True
                break
            if message.isdigit():
                break