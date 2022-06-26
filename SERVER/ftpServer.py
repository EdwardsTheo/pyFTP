import socket
from threading import Thread
from tkinter.tix import Select
import os, bcrypt, glob
import sys
import pickle

sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\SRCFTP\\pyFTP\\')
sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\SRCFTP\\pyFTP\\SQL')
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
        #client.send('ASK PSEUDO'.encode('utf-8'))
        client.send('ASK PSEUDO'.encode('utf-8'))
        thread = Thread(target=update_chat, args=(client,))
        thread.start()


# thread permettant de traiter les informations recues par les clients
def update_chat(client):
    while True:
        msg = ''
        msg = message = client.recv(1024)
        text = msg.decode('utf-8')
        c_input = text.split(" ")
        print(c_input)
        if c_input[0] == "LOG":
            if c_input[1] == "PSEUDO":
                req_serv = cmd_pseudo(client, c_input[2])
                send_message(client, "ASK PASSWORD")
                i = 0
            elif c_input[1] == "PASSWORD":
                print(i)
                userInfo = req_serv # Take back the info of the user taken previously
                req_serv = cmd_pass(c_input[2], userInfo, i)
                i = req_serv[0]
                send_message(client, req_serv[1])
        elif c_input[0] == "LIST":
            req_serv = cmd_list()
        elif c_input[0] == "SEND":
            print("SEND")
        elif c_input[0] == "GET":
            print("GET")
        elif c_input[0] == "DEL":
            print("DEL")
        #client.send(req_serv.encode("utf-8"))


def cmd_list(directory, userInfo) :
    #CHECK IF DIRECTORY EXIST
    
    # CHECK IF THE USER AS THE CORRECT RIGHT 

def cmd_pseudo(client, pseudo):
    userInfo = SELECT.sql_select_info_user(pseudo)
    userInfo = pseudo_exist(client, userInfo)
    if userInfo != 1:
        userInfo = check_ban(client, userInfo)
    return userInfo


def pseudo_exist(client, userInfo):
    if not userInfo:
        send_message(client, "ERROR PSEUDO 1")
        test = 1
        return test
    else:
        return userInfo


def check_ban(client, userInfo):
    if userInfo[0][7] == 1:
        send_message(client, "ERROR PSEUDO 2")
    else:
        return userInfo

def cmd_pass(input, userInfo, i):
    password = userInfo[0][4]
    check = bcrypt.checkpw(input.encode("utf-8"), password.encode("utf-8"))
    if check:
        command = 'SUCCESS 0'
    else:
        if i == 3:
            # Ban l'user
            MODIFY.update_status_ban(userInfo[0][1], 1)
            command = "ERROR PASS 1"
        else:
            command = "ERROR PASS 0"
            i = i + 1
    command = [i, command]
    return command


def send_message(client, command):
    client.send(command.encode('utf-8'))


def create_file(userInfo, filename):
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


def cmd_list(userInfo):
    city = SELECT.select_id_site(userInfo)
    directory = "C:\\Users\\bapti\\Desktop\\SRC_FTP-master\\Serveur_Storage\\" + city[0][0]
    os.chdir(directory)
    fake_list = "LIST: "
    for file in glob.glob("*"):
        fake_list = fake_list + file
    return fake_list


def cmd_list_adm():
    print("function cmd_list_adm")
    command = "Please choose the directory you want to list"
    return command


def cmd_get(command):
    command = "GET: Give the path of the file you want to receive:"
    return command


# appelle de la méthode main
print('Server is Listening ...')
main()
