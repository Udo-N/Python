from socket import *

# Create server socket with port number 10410
serverPort = 10410
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# Declaring variables for messages that will be sent back to client
okMessage = '200 OK\n'
errorMessage = 'Invalid command\n'
motd = 'This is the message of the day\n'

# Declaring variable for message that gets received from MSGSTORE command
clientMessage = ''

print('the server is ready to receive')
connectionSocket, addr = serverSocket.accept()                  # Open connection socket to receive from client

# Server stays active receiving from client until END command is received
while True:
    command = connectionSocket.recv(1024).decode()              # Receive command from client
    print("Command from client: '" + command + "'\n")           # Print command received from client

    # MSGGET command causes server send message of the day (motd) to client
    if command == 'MSGGET':
        connectionSocket.send(okMessage.encode())
        connectionSocket.send(motd.encode())
    # MSGSTORE command causes server to receive a message from client and store in the 'clientMessage' variable
    elif command == 'MSGSTORE':
        connectionSocket.send(okMessage.encode())
        clientMessage = connectionSocket.recv(1024).decode()
        connectionSocket.send(okMessage.encode())
    # END command breaks the while loop and closes the server connection
    elif command == 'END':
        connectionSocket.send(okMessage.encode())
        break
    # If command is not one of the above 3 commands, an error message is sent back to the client
    else:
        connectionSocket.send(errorMessage.encode())

serverSocket.close()                                            # Close server socket
