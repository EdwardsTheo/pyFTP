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
        print("The server is not responding")
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
                message = input("")
                message = "pseudo:" + message
                client.send(message.encode('utf-8'))
            elif message == 'Please write your password':
                password = input("")
                password = "password:" + password
                client.send(password.encode('utf-8'))
            elif message == "ftp_server$>" :
                send = input("")
                client.send(send.encode('utf-8'))
            elif message == "Provide an existing user" :
                client.close()
                exit()
            elif message == "Wrong password" :
                password = input("")
                password = "password:" + password
                client.send(password.encode('utf-8'))
                #client.close()
                #exit()
            elif message == "Connection abandonned because of too many failures" :
                client.close()
                exit()
            elif message == "Write a command :" :
                command = input("")
                if command == "SEND" :
                    print('Please give the path of the file you want to transfer')
                    file_transfer = input("")
                    test = os.path.exists(file_transfer)
                    if test :
                        filename = file_transfer.split("\\")
                        filename = filename[-1]
                        data = "FILE TO SEND:" + filename
                        print(data)
                        client.send(data.encode("utf-8"))
                    else : 
                        print("The file doesnt exist !")
                elif command == "GET" : 
                    client.send(command.encode("utf-8"))
            elif message == "SEND" :
                file = open(file_transfer, "rb") # opening for [r]eading as [b]inary
                data = file.read() # if you only wanted to read 512 bytes, do .read(512)
                file.close()
                print(data)
                client.send("FILE DATA:".encode("utf8") + data)         
            else : 
                text = message.split(":")
                if text[0] == "HELP" :
                    print(text[1])
                elif text[0] == "LIST" :
                    i = len(text)
                    if i == 1 :
                        print("There is no file in this directory")
                    else :
                        for y in range(1, i) : 
                            print("Fichier : " + text[y])
                elif text[0] == "GET" :
                    file = input("")
                    client.send(file.encode)

                command = input("ftpserver$> ")
                client.send(command.encode("utf-8"))
            # Deux choix, soit le client envoie une réponse, soit il traite la réponse du serveur 
            
        except Exception as e:
            print(e)
            exc_type, e, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
#write_thread = threading.Thread(target=write)
#write_thread.start()





