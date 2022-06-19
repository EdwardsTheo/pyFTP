from ctypes import sizeof
from pickle import TRUE
import socket
from sqlite3 import connect
import threading
from threading import Thread
from datetime import datetime
# from colorama import Fore, init, Back
import random
import os, sys


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5002))

stop_thread = False

# Test connection
def try_connect():
    a_socket = socket.socket()
    try:
        a_socket.connect(("127.0.0.1", 5002))  # Tente de se connecter à l'adresse IP et au port suivant
        a_socket.shutdown(socket.SHUT_RDWR)  # Essaye de se deconnecter du client ? verif que ça marche côté serveur
        a_socket.close()
    except:
        print("Le serveur ne répond pas")
        return False



def client_connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5002))

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            if message == "Please write your pseudo" :
                message = "fpires"
                message = "pseudo:" + message
                client.send(message.encode('utf-8'))
            elif message == 'Please write your password':
                password = input("")
                password = "password:" + password
                client.send(password.encode('utf-8'))
        except :
            print("error with the server")
            client.close()
            break

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()