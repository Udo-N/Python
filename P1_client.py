from socket import *

# Client prompts user to input IP address of the server, if the IP adress is not found,
# there is an error message and the user is prompted to re-enter the IP address
while True:
    try:
        # Create client socket from user inputted IP address
        serverName = input('Input Server IP address: ')
        serverPort = 10410
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
    except:
        print("Server not found\n")
        continue
    break
print("Server found\n")

# Client keeps sending message to server until END command is sent
while True:
    sentence = input('Input command: ')
    clientSocket.send(sentence.encode())                # Send command to server
    serverMessage = clientSocket.recv(1024)             # Receive ok message from server
    print('From Server:', serverMessage.decode())       # Print ok message from server

    # MSGGET command receives the message of the day from server and prints it
    if sentence == 'MSGGET':
        serverMessage = clientSocket.recv(1024)
        print(serverMessage.decode())
    # MSGSTORE command sends a message to the server and receives ok message
    elif sentence == 'MSGSTORE':
        message = input('Input message: ')
        clientSocket.send(message.encode())
        serverMessage = clientSocket.recv(1024)
        print(serverMessage.decode())
    # END command receives ok message from server and breaks the while loop, closing the connection
    elif sentence == 'END':
        serverMessage = clientSocket.recv(1024)
        print(serverMessage.decode())
        break

clientSocket.close()                                    # Close client socket
