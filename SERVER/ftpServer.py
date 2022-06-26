import json
import pickle

import bcrypt
import glob
import os
import socket
import sys
from threading import Thread
from os import listdir
from os.path import isfile, join

from SQL.SELECT import select_id_site

sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\pyFTP\\')
sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\pyFTP\\SQL')
from SQL import SELECT, MODIFY

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
        # client.send('ASK PSEUDO'.encode('utf-8'))
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
                userInfo = req_serv  # Take back the info of the user taken previously
                req_serv = cmd_pass(c_input[2], userInfo, i)
                i = req_serv[0]
                send_message(client, req_serv[1])
        elif c_input[0] == "LIST":
            req_serv = cmd_list(c_input[1], userInfo)
            if type(req_serv) != list:
                send_message(client, req_serv)
            else:
                send_message_list(client, req_serv)
        elif c_input[0] == "SEND":
            req_serv = create_file(c_input[1], c_input[2], c_input[3], userInfo)
            send_message(client, req_serv)
        elif c_input[0] == "GET":
            print("GET")
        elif c_input[0] == "DEL":
            print("DEL")
            cmd = c_input[1].split("/")
            delete_file(cmd)
        # client.send(req_serv.encode("utf-8"))


def cmd_list(directory, userInfo):
    cmd = ""
    if directory == "/": directory = ""
    directory = directory.upper()
    path = 'C:\\Users\\bapti\\Desktop\\pyFTP\\Serveur_Storage\\' + directory
    # CHECK IF DIRECTORY EXIST
    check = check_directory(directory, path)
    if check:
        check = check_right(directory, userInfo)
        if check:
            cmd = os.listdir(path)
            cmd.insert(0, "SUCCESS")
            cmd.insert(1, "4")
        else:
            cmd = "ERROR LIST 1"
    else:
        cmd = "ERROR LIST 0"
    return cmd


def check_directory(directory, path):
    isFile = os.path.isdir(path)
    return isFile


def check_right(directory, userInfo):
    check = True
    cityName = select_id_site(userInfo[0][5])
    cityName = cityName[0][0]
    if cityName != "PARIS":
        if cityName != directory:
            check = False
    return check


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
    print("send message")


def send_message_list(client, command):
    command = ' '.join(command)
    client.send(command.encode("utf-8"))


def delete_file(cmd) :


def create_file(filename, file_data, directory, userInfo):
    path = 'C:\\Users\\bapti\\Desktop\\pyFTP\\Serveur_Storage\\'
    check = check_directory(directory, path)
    if check:
        check = check_right(directory, userInfo)
        if check:
            path = create_copy(path, directory, filename)
            print(path)
            with open(path, 'w') as f:
                f.write(file_data)
            cmd = "SUCCESS 2"
        else:
            cmd = "ERROR LIST 1"
    else:
        cmd = "ERROR LIST 0"
    return cmd


def create_copy(path, directory, filename):
    first_path = path
    path = path + directory + "\\" + filename
    isFile = os.path.isfile(path)
    if isFile:
        filename = filename.split(".")
        filename = filename[0] + "(1)" + "." + filename[1]
        path = first_path + directory + "\\" + filename
        path = loop_copy(path, first_path, directory)
    return path


def loop_copy(path, first_path, directory): # Permet de créer des copies à l'infini
    isFile = os.path.isfile(path)
    i = 1
    while isFile :
        head, tail = os.path.split(path)
        filename = tail
        filename = filename.split(".")
        print(filename)
        new_filename = filename[0].split(filename[0][-3:])
        new_copy = "(" + str(i) + ")"
        new_filename = new_filename[0] + new_copy
        path = first_path + directory + "\\" + new_filename + "." + filename[1]
        i = i + 1
        isFile = os.path.isfile(path)
    return path

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
