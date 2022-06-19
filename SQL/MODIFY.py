from CONNECT import *

def sql_update_user(first_name,last_name,pseudo,passwd,city,ban,id) :
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users set fName = ?, lName = ?, login = ?, password = ?, site = ?, role = ?, ban = ? where users_id = ?",
                (first_name, last_name, pseudo, passwd, city, '1', ban, id))
    conn.commit()
    conn.close()

def update_status_ban(id, command) :
    print(command)
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET ban = ? WHERE users_id = ?",
               (command,id))
    conn.commit()
    conn.close()

def update_password(id, password) :
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE users_id = ?",
               (password,id))
    conn.commit()
    conn.close()
