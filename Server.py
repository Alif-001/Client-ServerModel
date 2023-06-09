import socket
import threading

import matplotlib.pyplot as plt

# localhost
host = "127.0.0.1"
# do not take any reserved or well known ports
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
banned_words = ["bad", "idiot", "black"]

brand_name = ["Apple", "Google", "Microsoft", "Windows"]
brand_count = {}
for i in brand_name:
    brand_count[i] = 0

# braodcasting messages from the server to all the clients


def broadcast(message):
    # implement the filtering of the messages here
    for i in banned_words:
        if i in message.decode('ascii'):
            message_str = message.decode('ascii')
            message_str = message_str.replace(i, '*' * len(i))
            message = message_str.encode('ascii')

    # implement the brand analytics and tracking here
    # brand analytics
    for brand in brand_name:
        messageDecode = message.decode('ascii')
        if brand in messageDecode:
            brand_count[brand] += 1

    # tracking
    with open('chatTracking.txt', 'a')as f:
        f.write(f'{(message.decode("ascii"))}\n')

    for client in clients:
        client.send(message)


def handle(client):
    # Running an infinite loop here
    while True:
        try:
            # receiving 1024 bytes
            message = client.recv(1024)
            print(message)
            broadcast(message)

        except:
            # find out the index of the failed client frm the clients list
            index = clients.index(client)
            clients.remove(client)
            client.close()
            # we also remove the nickname of the removed client
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break

    brand_counts()

# This is the method that runs first


def receive():

    # Accepting all the connections
    while True:
        print("receive function is running on the server!")
        # returns a tuple
        # returns the client and the address of the client
        client, address = server.accept()

        # you have cut down the address str type casting
        print(f"Connected with {str(address)}")

        # we need to ask the client for the nickname
        # made change here
        name = "NICK"
        client.send(name.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")

        broadcast(f"{nickname} joined the chat".encode('ascii'))
        # letting know the specific client that it has connected to the server
        client.send("Connected to the server".encode('ascii'))

        # Implementation of a log that keeps record of all the usernames so far.
        with open("usernames.txt", "a") as f:
            f.write(f"{nickname}\n")

        # define and run a thread
        # because we want to be able to handle multi clients same time

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def brand_counts():
    bar_colors = ['red', 'blue', 'green', 'orange']
    plt.bar(range(len(brand_count)), list(
        brand_count.values()), color=bar_colors)
    plt.xticks(range(len(brand_count)), list(brand_count.keys()))
    plt.xlabel("Brands")
    plt.ylabel("Mentions")
    plt.title("Brand analytics")
    plt.show()


# main method
print("Server is listening..........")
receive()
