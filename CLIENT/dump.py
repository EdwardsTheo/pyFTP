elif message == "SEND":
file = open(file_transfer, "rb")  # opening for [r]eading as [b]inary
data = file.read()  # if you only wanted to read 512 bytes, do .read(512)
file.close()
print(data)
client.send("FILE DATA:".encode("utf8") + data)
elif message == "Please choose the directory you want to list":
show_avaiable_city()
elif message == "ftp_server$> ":
command = basic_prompt()
if command == "SEND":
    file_transfer = cmd_send()
    command == "noting"
    client.send("LIST".encode("utf-8"))
elif command == "GET":
    client.send(command.encode("utf-8"))
elif command == "HELP":
    cmd_help()
    command = input("ftp_server$> ")
elif command == "LIST":
    print("hello")
    client.send("LIST".encode("utf-8"))
elif command == "DEL":
    print("DEL")
else:
    client.send(command=input(""))







  if message == "Please write your pseudo":
                message = input("Pseudo : ")
                message = "pseudo:" + message
                client.send(message.encode('utf-8'))
            elif message == 'Please write your password':
                password = input("Password : ")
                password = "password:" + password
                client.send(password.encode('utf-8'))
            elif message == "Provide an existing user":
                client.close()
                exit()
            elif message == "Wrong Password":
                print(message)
                password = input("")
                password = "password:" + password
                client.send(password.encode('utf-8'))
                # client.close()
                # exit()
            elif message == "Connection abandonned because of too many failures":
                print(message)
                client.close()
                exit()