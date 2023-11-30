import threading
import socket
import sys
import os
from datetime import datetime

nickname = input("Please enter your name: ")
threads = []
#To start the connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

COLOR_RESET = '\033[0m'
COLOR_YELLOW = '\033[93m'

#to recieve and send message from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message == 'QUIT':
                sys.exit(2)
            else:
                #print(message)
                 print(parse_formatted_message(message))
        except Exception as e:
            print('Server is not responding')
            client.close()
            sys.exit(2)

def write():
    while True:
        message = '{} {}'.format(nickname, input(''))
        try:
            client.send(message.encode('utf-8'))
        except:
            sys.exit(0)
            
#Time
def parse_formatted_message(message):
    timestamp = datetime.now().strftime("%H:%M:%p")
    if '[personal message]' in message:
        return f"[{COLOR_YELLOW}{timestamp}] {message}{COLOR_RESET}"
    else:
        return f"[{timestamp}] {message}"
    
receive_thread = threading.Thread(target=receive)
receive_thread.start()
threads.append(receive_thread)
write_thread = threading.Thread(target=write)
write_thread.start()
threads.append(write_thread)