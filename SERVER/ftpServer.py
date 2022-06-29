import logging
import os
import socket
import sys
from datetime import date
from threading import Thread

import bcrypt

from SQL.SELECT import select_id_site

sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\pyFTP\\')
sys.path.insert(1, 'C:\\Users\\bapti\\Desktop\\pyFTP\\SQL')
from SQL import SELECT, MODIFY

# Adresse IP du serveur
HOST = "127.0.0.1"
PORT = 5002  # port du serveur

today = date.today()
d = today.strftime("%d_%m_%Y")
logfile = "C:\\Users\\bapti\\Desktop\\pyFTP\\LOG\\STORAGE\\" + "ftpserver_log_" + d + ".log"
logging.basicConfig(filename=logfile,
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()

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
        logger.setLevel(logging.INFO)
        logger.info("Connected with " + str(address))
        client.send('ASK PSEUDO'.encode('utf-8'))
        thread = Thread(target=update_chat, args=(client,))
        thread.start()


# thread permettant de traiter les informations recues par les clients
def update_chat(client):
    while True:
        try :
            msg = ''
            msg = message = client.recv(1024)
            text = msg.decode('utf-8')
            c_input = text.split(" ")
            print("---------")
            print(c_input)
            print("---------")
            if text == "": exit()
            if c_input[0] == "LOG":
                if c_input[1] == "PSEUDO":
                    req_serv = cmd_pseudo(client, c_input[2])
                    send_message(client, "ASK PASSWORD")
                    i = 0
                    userInfo = req_serv
                elif c_input[1] == "PASSWORD":
                    req_serv = cmd_pass(c_input[2], userInfo, i, client)
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
                req_serv = get_file(c_input[1], c_input[2], userInfo, client)
                send_message(client, req_serv)
            elif c_input[0] == "DEL":
                print("DEL")
                cmd = c_input[1].split("/")
                req_serv = delete_file(userInfo, cmd)
                send_message(client, req_serv)
        except Exception as e:
            print(e)
            exc_type, e, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            exit()


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


def check_file(directory, path):
    isFile = os.path.isfile(path)
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


def cmd_pass(input, userInfo, i, client):
    print("-----------")
    print(userInfo)
    print("-----------")
    password = userInfo[0][4]
    check = bcrypt.checkpw(input.encode("utf-8"), password.encode("utf-8"))
    if check:
        print(input)
        command = 'SUCCESS 0'
        logger.setLevel(logging.INFO)
        logger.info("The user " + userInfo[0][3] + " successfully logged into the server")
    else:
        if i == 2:
            # Ban l'user
            # MODIFY.update_status_ban(userInfo[0][0], 1) # TODO
            command = "ERROR PASS 0"
            logger.setLevel(logging.CRITICAL)
            logger.critical("The user " + userInfo[0][3] + " missed is password 3 times, he has been banned")
        else:
            command = "ERROR PASS 0"
            i = i + 1
    command = [i, command]
    return command


def send_message(client, command):
    print(command)
    client.send(command.encode('utf-8'))
    print("send message")


def send_message_list(client, command):
    command = ' '.join(command)
    client.send(command.encode("utf-8"))


def delete_file(userInfo, cmd):
    path = 'C:\\Users\\bapti\\Desktop\\pyFTP\\Serveur_Storage\\'
    directory = cmd[1]
    check = check_directory(directory, path)
    if check:
        check = check_right(directory, userInfo)
        if check:
            path = path + directory + "\\" + cmd[2]
            os.remove(path)
            logger.setLevel(logging.INFO)
            logger.info("The user " + userInfo[0][3] + " deleted the file :" + cmd[2])
            cmd = "SUCCESS 3"
        else:
            cmd = "ERROR DEL 1"
    else:
        cmd = "ERROR DEL 0"
    return cmd


def get_file(directory, file_destination, userInfo, client):
    new_dir = directory.split('/')
    directory = new_dir[0] + "\\" + new_dir[1]
    path = "C:\\Users\\bapti\\Desktop\\pyFTP\\Serveur_Storage\\"
    directory = path + directory
    check = check_directory(directory, path)
    if check:
        check = check_right(directory, userInfo)
        if check:
            data = get_file_data(directory)
            head, tail = os.path.split(directory)
            name_file = tail
            cmd = "SUCCESS 1 " + name_file + " " + data + " " + file_destination
            logger.setLevel(logging.INFO)
            logger.info("The user " + userInfo[0][3] + " downloaded the file :" + new_dir[1])
            return cmd
        else:
            cmd = "ERROR GET 1"
    else:
        cmd = "ERROR GET 0"
    return cmd


def get_file_data(path):
    with open(path, 'r') as file:
        data = file.read()
    return data


def create_file(filename, file_data, directory, userInfo):
    path = 'C:\\Users\\bapti\\Desktop\\pyFTP\\Serveur_Storage\\'
    check = check_directory(directory, path)
    if check:
        check = check_right(directory, userInfo)
        if check:
            path = create_copy(path, directory, filename)
            with open(path, 'w') as f:
                f.write(file_data)
            cmd = "SUCCESS 2"
            logger.setLevel(logging.INFO)
            logger.info("The user " + userInfo[0][3] + " imported the file :" + filename)

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


def loop_copy(path, first_path, directory):  # Permet de créer des copies à l'infini
    isFile = os.path.isfile(path)
    i = 1
    while isFile:
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


# appelle de la méthode main
print('Server is Listening ...')
main()
