import random
import socket
import threading

nickname = input("Choose your nickname before joining server: ")

# defining a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# this is the ip of the server that we want to connect to
client.connect(('127.0.0.1', 55555))


def receive():
    # always tries to receive data from the server
    while True:
        try:
            # receiving from the server
            message = client.recv(1024).decode('ascii')
            if (message == 'NICK'):
                client.send(nickname.encode('ascii'))

            else:
                print(message)

        except:
            (print("An error occured!"))
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# we are running 2 threads receive thread and the write thread

# the thread for receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()