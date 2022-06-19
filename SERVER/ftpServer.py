import socket
from threading import Thread
from tkinter.tix import Select
import os, bcrypt, glob
import sys
import pickle
sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\SRC_FTP-master')
sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\SRC_FTP-master\\SQL')
from SQL import SELECT, MODIFY
from colors import Color


# Adresse IP du serveur
HOST = "127.0.0.1"
PORT = 5002  # port du serveur

# initialise une liste de tous les clients connecté au socket
client_sockets = set()
MySocket = socket.socket()  # on cré un socket tcp
MySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                    1)  # on rend le port reutilisable pour que plusieurs clients puisse s'y connecter
MySocket.bind((HOST, PORT))  # associe le socket à l'adresse qu'on utilise
MySocket.listen()  # le socket est en attente de connection, il y aura maximum 42 connections
print(f"[*] Listening as {HOST}:{PORT}")

# initialisation des listes permettant l'identification des différents clients dans le chat bot
clients = list()  # list de clients connectés
nicknames = list()  # list des pseudos connectés

def main():
    while True:
        client, address = MySocket.accept()
        print("Connecté avec " + str(address))
        client.send('Please write your pseudo'.encode('utf-8'))
        #client.send('Write a command :'.encode('utf-8'))
        thread = Thread(target=update_chat, args=(client,))
        thread.start()


# thread permettant de traiter les informations recues par les clients
def update_chat(client):
    while True:
            msg = ''
            msg = message = client.recv(1024)
            text = msg.decode('utf-8')
            foutput = text.split(":")
            userInfo = SELECT.sql_select_info_user("btheobald")
            print(foutput)
            print(foutput[0])
            if foutput[0] == "pseudo" :
                command = prompt_pseudo(foutput, userInfo)
                client.send(command.encode("utf-8"))
                i = 0
            elif foutput[0] == "password" : 
                command = prompt_password(foutput, userInfo, i)
                print (command)
                client.send(command.encode("utf-8"))
            if text == "GET" :
                command = cmd_get(command)
                client.send(command.encode("utf-8")) 
            elif text == "LIST" :
                command = cmd_list(userInfo)
                client.send(command.encode("utf-8"))
            elif text == "HELP" :
                command = cmd_help(command)
                client.send(command.encode("utf-8"))
            if foutput[0] == "FILE TO SEND" :
                filename = foutput[1]
                client.send('SEND'.encode("utf-8"))
            elif foutput[0] == "FILE DATA" :
                create_file(userInfo, filename)
    
def prompt_pseudo(command, userInfo) :
    userInfo = SELECT.sql_select_info_user(command[1])
    if userInfo :
        print(userInfo)
        if userInfo[0][7] == 1 : 
            command = "You are banned"
        else :
            command = "Please write your password"        
    else :
        command = 'Provide an existing user'
                    
    return command 

def prompt_password(foutput, userInfo, i) : 
    print(i)
    password = userInfo[0][4]
    check = bcrypt.checkpw(foutput[1].encode("utf-8"), password.encode("utf-8"))
    if check : 
        command = 'You are connected ! Write your first command or write "HELP" so see all the avaible command'
    else :
        i = i + 1
        if i == 3 :
            #Ban l'user 
            MODIFY.update_status_ban(userInfo[1], 1)
            command = "Connection abandonned because of too many failures"
        else :
            command = "Wrong password"
    print(command)
    return command

def send_message(command, client) : 
    client.send(command.encode('utf-8'))

def create_file(userInfo, filename) :
    text = text.replace("FILE DATA:", "")
    print(text)
    city = SELECT.select_id_site(userInfo[0][5])
    directory = "C:\\Users\\bapti\\Desktop\\SRC_FTP-master\\Serveur_Storage\\" + city[0][0] + "\\" + filename
    text_file = open(directory, "w")
 
    text_file.write(text)

    text_file.close()

    # first get all lines from file
    with open(directory, 'r') as f:
        lines = f.readlines()
    # remove spaces
        lines = [line.replace(' ', '') for line in lines]
    # finally, write lines in the file
        with open(directory, 'w') as f:
            f.writelines(lines)

def cmd_list(userInfo) :
    city = SELECT.select_id_site(userInfo[0][5])
    directory = "C:\\Users\\bapti\\Desktop\\SRC_FTP-master\\Serveur_Storage\\" + city[0][0]
    os.chdir(directory)
    fake_list = "LIST: "
    for file in glob.glob("*"):
        fake_list = fake_list + file
    return fake_list

def cmd_help(command) : 
    command = "HELP: *****List of all the command**** \n SEND -> Send a file to serveur, please indicate the location of your file \n LIST -> List all the file in your city directory \n GET -> Download a file from the city directory, please indicate the name of the file and where you want to store it"
    return command

def cmd_get(command) : 
    command = "GET: Give the path of the file you want to receive:"
    return command


# appelle de la méthode main
print('Server is Listening ...')
main()
