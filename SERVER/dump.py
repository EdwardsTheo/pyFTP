userInfo = SELECT.sql_select_info_user()
        print(len(c_input))
        if c_input[0] == "pseudo":
            command = prompt_pseudo(c_input, userInfo)
            i = 0
        elif c_input[0] == "password":
            command = prompt_password(c_input, userInfo, i)
            test = isinstance(command, int)
            if test:
                i = i + 1
                command = "Wrong Password"
        elif c_input[0] == "LIST":
            if len(c_input) == 1 :
                print(userInfo[0][6])
                if userInfo[0][6] == 0 :
                    print("True")
                    command = cmd_list_adm()
            else :
                print("oh")
                command = "ftp_server$> "
        if text == "GET":
            command = cmd_get(command)
        if c_input[0] == "FILE TO SEND":
            filename = c_input[1]
            command = "SEND"
        elif c_input[0] == "FILE DATA":
            create_file(userInfo, filename)
        print("final command")
        print(command)
        print("-----")
        client.send(command.encode("utf-8"))