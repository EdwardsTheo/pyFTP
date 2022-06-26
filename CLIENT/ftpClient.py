import pickle
from ctypes import sizeof
from pickle import TRUE
import socket
from sqlite3 import connect
import threading
from getpass import getpass
from threading import Thread
from datetime import datetime
# from colorama import Fore, init, Back
import random
import os, sys

from SQL import SELECT

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
            # print(client.recv(1024))
            msg = client.recv(1024).decode('utf-8')
            cmd = msg.split(" ")
            print("-----")
            print(cmd)
            print("------")
            # Command ask by the client
            if cmd[0] == "SUCCESS":  # Prompt to launch command
                success_print(client, cmd)
            elif cmd[0] == "ERROR":
                if cmd[1] == "PSEUDO":
                    error_pseudo(cmd[2])
                    exit()
                elif cmd[1] == "PASS":
                    cmd = error_pass(cmd[2])
                elif cmd[1] == "LIST":
                    error_list(client, cmd[2])
            elif cmd[0] == "ASK":
                if cmd[1] == "PSEUDO":
                    cmd = ask_pseudo()
                elif cmd[1] == "PASSWORD":
                    cmd = ask_password()
            print("--- INPUT SEND TO SERVER-----")
            print(cmd)
            send_input(cmd, client)
            print("-----------------------------")

        except Exception as e:
            print(e)
            exc_type, e, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


def sort_cmd(client):
    cmd = ask_input()
    print(cmd)
    cmd = cmd.split(" ")
    print("command asked")
    print(cmd)
    print("------")
    if cmd[0] == "HELP":
        cmd_help()
    elif cmd[0] == "LIST":
        cmd_list(client, cmd)
        receive()
    elif cmd[0] == "SEND":
        cmd_send(client, cmd)
        receive()
        print("send")
    elif cmd[0] == "GET":
        print("get")
    elif cmd[0] == "DEL":
        cmd.append("/PARIS/file_transfer(1).txt")
        cmd_del(client, cmd)
        receive()
    else:
        print("Please select an existing command or press HELP")
    sort_cmd(client)


def success_print(client, code):
    if code[1] == "0":
        print("You are connected ! Press HELP, to see all the avaiable command")
    elif code[1] == "2":
        print("The file has been sent")
    elif code[1] == "4":
        print_list(code)
    sort_cmd(client)


def print_list(code):
    del code[0:2]
    print("Result of the list command :")
    for elem in code:
        print("----> " + elem)


def ask_pseudo():
    print("Authentificate with your pseudo to connect to the server")
    # cmd = ask_input()
    cmd = "btheobald"
    cmd = "LOG PSEUDO " + cmd
    return cmd


def ask_password():
    print("Enter your password")
    # cmd = ask_input()
    cmd = "Abracadabra@92"
    cmd = "LOG PASSWORD " + cmd
    return cmd


def error_pseudo(code):
    if code == "1":
        print("The user doesn't exist")
    elif code == "2":
        print("You are banned")
    exit()


def error_list(client, code) :
    if code == "0":
        print("The directory doesn't exist")
    elif code == "1":
        print("You don't have the authorizations to inspect this directory")
    sort_cmd(client)


def error_pass(code):
    if code == "0":
        print("Wrong password, send it again")
        cmd = ask_input()
        cmd = "LOG PASSWORD " + cmd
        return cmd
    elif code == "1":
        print("Two many failures, the account has been banned, check with your local administrators")
        exit()


def cmd_send(client, cmd):
    print(cmd)
    len_cmd = len(cmd)
    if len_cmd != 3:
        print("Missing parameters, press HELP to hava the command details")
        sort_cmd(client)
    else:
        if cmd[1] == "" or cmd[2] == "":
            print("Incorrect parameters")
            sort_cmd(client)
        else:
            path = cmd[1]
            check = check_file(path)
            if check:
                data = get_file_data(path)
                head, tail = os.path.split(path)
                name_file = tail
                send_input("SEND " + name_file + " " + data + " " + cmd[2], client)
            else:
                print("The file that you want to send don't exist")
                sort_cmd(client)


def check_file(path):
    isFile = os.path.isfile(path)
    return isFile


def get_file_data(path):
    with open(path, 'r') as file:
        data = file.read()
    return data


def cmd_del(client, cmd):
    len_cmd = len(cmd)
    if len_cmd != 1:
        print("Missing one parameters")
        sort_cmd(client)
    else:
        if cmd[1] == " ":
            print("Incorrect parameters")
            sort_cmd(client)
        else:
            send_input("DEL " + cmd[1], client)


def cmd_list(client, cmd):
    len_cmd = len(cmd)
    if len_cmd != 2:
        print("Missing one parameters")
        sort_cmd(client)
    else:
        if cmd[1] == " ":
            print("Incorrect parameters")
            sort_cmd(client)
        else:
            send_input("LIST " + cmd[1], client)


def ask_input():
    msg = input("ftp_server$> ")
    return msg


def send_input(command, client):
    client.send(command.encode("utf-8"))


def cmd_help():
    print("-> EXIT : Exit the program")
    print("-> LIST : List the files in your company directory")
    print("---Use : LIST {path of the directory")
    print("-> SEND : Send a file in your company directory")
    print("----Use : SEND {path of the directory/file} {remote path of the directory}")
    print("-> GET  : Get a file from your company directory")
    print("----Use : GET {path of the directory/file} {path of the local directory}")
    print("-> DEL  : Delete the file form your company directory")
    print("----Use : DEL {path of the directory/file}")


def basic_prompt():
    message = input("ftp_server$> ")
    return message


def show_avaiable_city():
    city = SELECT.sql_show_city()
    for rows in city:
        print("\nThe Directory available are :    " + str(rows[0]))


recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
# write_thread = threading.Thread(target=write)
# write_thread.start()
