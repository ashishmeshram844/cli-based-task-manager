"""
Daily task management console based
- create alias of command and run from anywhere
    - add - create new task
    - update - update a provided id task
    - delete - delete a provided id task
    - list - list all tasks
"""

import sys
import sqlite3
from prettytable import PrettyTable
import getpass
import hashlib
import os 
import signal

conn = sqlite3.connect('/home/ashish/Desktop/personal_projects/my-work/daily_tasks.db')

class UserManagement(object):
    def __init__(self):
        pass

    def create_user_table(self,cursor):
        """
        Responsible to create a users table if not available in database
        """
        table_name = "Users"
        columns = "(id INTEGER PRIMARY KEY AUTOINCREMENT, datetime DATETIME DEFAULT CURRENT_TIMESTAMP, username TEXT, password TEXT)"
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} {columns}"
        cursor.execute(create_table_query)
        conn.commit()
        
    def test_user(self):
        print("test user")

    def create_user(self,username,password):
        """
        This function creates a new user 
        """
        try:    
            if username != "ashishmeshram844":
                if not self.check_user_is_avail(username):
                    password = Encryption().hash_password(password)
                    result = self.cursor.execute("INSERT INTO Users (username,password) VALUES (?,?)", (username,password))
                    conn.commit()
                    print("\033[32m User Created Successfully  \033[0m")
                else:
                    print("\033[31m User is Already Registered !  \033[0m")
            else:
                print("\033[31m User is Already Registered !  \033[0m")
        except Exception as e:
            print("\033[31m Failed to crate a new User !  \033[0m")

    def fetch_all_users(self):
        """
        This function get al data from Users table
        """
        result = self.cursor.execute("SELECT * FROM Users ORDER BY id DESC").fetchall()
        return result

    def list_users(self):
        """ 
        This function display all users data
        """
        try:
            users_data = self.fetch_all_users()
            table = PrettyTable()
            table.field_names = ["ID", "DATE", "USERNAME","PASSWORD"]
            for row in users_data:
                table.add_row([row[0], row[1], row[2], row[3]])
            table.max_width = 80
            table.align = 'l'
            print(table)
        except Exception as e:
            print("\033[31m Failed to Load Users List !  \033[0m")

    def check_user_is_avail(self,username):
        row = self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
        return not row is None

    def delete_user(self,username):
        try:
            if self.check_user_is_avail(username):
                self.cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
                conn.commit()
                print("\033[32m User Deleted Successfully  \033[0m")
            else:
                print("\033[31m User is not Available | Failed to delete  !  \033[0m")
        except Exception as e:
            print("\033[31m Failed to Delete User  !  \033[0m")


    def create_user_inputs(self):
        username = str(input("Enter Username : "))
        password = str(input("Enter Password : "))
        return username,password

    def user_operation_handle(self,splitted_operations):
        """
        This function handle operations on user module
        """
        if splitted_operations[0] in self.available_operations:
            match splitted_operations[0]:
                case 'add':
                    try:
                        if len(splitted_operations) == 1:
                            user_data = self.create_user_inputs()
                            self.create_user(user_data[0],user_data[1])
                        else:
                            print("\033[31m Extra parameters not alowed while adding user !  \033[0m")
                    except Exception as e:
                        print("\033[31m Failed to create user !  \033[0m")
                case 'update':
                    print("Update User")
                case 'delete':
                    try:
                        if len(splitted_operations) == 1:
                            username = str(input("Enter username which you want to delete : "))
                            self.delete_user(username)
                        elif len(splitted_operations) == 2:
                            self.delete_user(splitted_operations[1])
                        else:
                            print("\033[31m Extra Parameters not alowd !  \033[0m")
                    except Exception as e:
                        print("\033[31m Failed to delete user !  \033[0m")
                case 'list':
                    if len(splitted_operations) == 1:
                        self.list_users()
                    else:
                        print("\033[31m No Extra parameters are allowed !  \033[0m")
                case _:
                    print("\033[31m Wrong Opeeration !  \033[0m")
        else:
            print("\033[33m This Operation is not allowd !  \033[0m")



    def user_module(self):
        print("\033[34m Switching to user Module...  \033[0m")
        module_status = True
        while module_status:
            operation = self.take_user_operation('user')
            if operation == "exit":
                print("User Module Closed")
                break
            splitted_operations = operation.split(" ")
            if operation == 'clear':
                os.system('clear')
            elif len(splitted_operations) <= 2:
                self.user_operation_handle(splitted_operations)
            else:
                print("\033[33m Cant use more than two arguments at a time !  \033[0m")


class WorkConsole(UserManagement):
    def __init__(self,username):
        
        self.username = username
        self.cursor = self.get_cursor()
        self.create_task_table(self.cursor)
        self.create_user_table(self.cursor)
        self.available_modules = ['user','task']
        self.available_operations = ['add','delete','update','list']

    def create_cursor(self,conn = conn):
        """
        Crates a cursor object for connection
        """
        cursor = conn.cursor()
        return cursor

    def create_task_table(self,cursor):
        """
        Create a Table where all tasks will be stored
        - created only when not available in db
        """
        table_name = "Tasks"
        columns = "(id INTEGER PRIMARY KEY AUTOINCREMENT, datetime DATETIME DEFAULT CURRENT_TIMESTAMP, task_detail TEXT,added_by TEXT)"
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} {columns}"
        cursor.execute(create_table_query)
        conn.commit()

    def get_cursor(self):
        """
        gives the cursor object 
        """
        cursor = self.create_cursor()
        return cursor
        
    def add_task(self,task):
        """
        Responsible to add new task in table
        """
        try:    
            result = self.cursor.execute("INSERT INTO Tasks (task_detail,added_by) VALUES (?,?)", (task,self.username))
            conn.commit()
            print("\033[32m Task Addedd Successfully  \033[0m")
        except Exception as e:
            print(e)
            print("\033[31m Failed to add Task !  \033[0m")

    def display_tasks(self,tasks_data):
        """
        Helper function which display all tasks list in tabular format
        """
        table = PrettyTable()
        table.field_names = ["ID", "DATE", "TASK DETAIL","ADDED BY"]
        for row in tasks_data:
            table.add_row([row[0], row[1], row[2],row[3]])
        table.max_width = 80
        table.align = 'l'
        print(table)
        
    def fetch_all_tasks(self):
        """
        get all tasks list
        """
        result = self.cursor.execute("SELECT * FROM Tasks ORDER BY id DESC").fetchall()
        return result

    def fetch_user_tasks(self):
        row = self.cursor.execute("SELECT * FROM Tasks WHERE added_by = ?", (self.username,)).fetchall()
        return row


    def list_tasks(self):
        """
        get all task list and display on screen
        """
        try:
            if self.username == 'ashishmeshram844':
                result = self.fetch_all_tasks()
            else:
                result = self.fetch_user_tasks()
            self.display_tasks(result)
        except Exception as e:
            print(e)
            print("\033[31m Failed to Load Tasks List !  \033[0m")

    def check_task_is_avail(self,task_id):
        """
        check inputed id value task is available in table or not
        """
        row = self.cursor.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,)).fetchone()
        return not row is None

    def delete_task(self,task_id):
        """
        Responsible to delete task which id is provided by user
        """
        try:
            if self.check_task_is_avail(task_id):
                self.cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
                conn.commit()
                print("\033[32m Task Deleted Successfully  \033[0m")
            else:
                print("\033[31m Task is not Available | Failed to delete  !  \033[0m")
        except Exception as e:
            print("\033[31m Failed to Delete Tasks  !  \033[0m")

    def update_task(self,task_id):
        """
        Update specific task which user provide id
        """
        if self.check_task_is_avail(task_id):
            row = self.cursor.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,)).fetchone()
            print("Task Detail : ",row[2])
            updated_task = str(input("Enter Updated Task Detail : "))
            update_query = """
                UPDATE Tasks
                SET task_detail = ?
                WHERE id = ?
            """
            task_detail = updated_task
            self.cursor.execute(update_query, (task_detail, task_id))
            conn.commit()
            print("\033[32m Task Updated Successfully  \033[0m")
        else:
            print("\033[31m Task is not Available | Failed to Update  !  \033[0m")

    def take_user_operation(self,mod_name):
        """
        This function takes input from user which want to perform operation
        """
        operation = str(input(f"work@ashish/{mod_name} : "))
        return operation

    def add_operation(self,splitted_operations):
        """
        Handle add new task operation
        """
        if len(splitted_operations) == 1:
            task = str(input("Enter a Task : "))
            self.add_task(task)
        else:
            print("\033[31m No extra parameter required in add !  \033[0m")

    def update_operation(self,splitted_operations):
        """
        Handle Update specific task operation task
        """
        try:
            if len(splitted_operations) == 2:
                self.update_task(splitted_operations[1])
            else:
                task_id = int(input("Enter task ID : "))
                self.update_task(task_id)
        except Exception as e:
            print("\033[31m Failed to update Task !  \033[0m")

    def delete_operation(self,splitted_operations):
        """
        Handle Delet Task operation
        """
        try:
            if len(splitted_operations) == 2:
                self.delete_task(splitted_operations[1])
            else:
                task_id = int(input("Enter Task ID : "))
                self.delete_task(task_id)
        except Exception as e:
            print("\033[31m Please Provide proper Id of task !  \033[0m")

    def task_operation_handle(self,splitted_operations):
        """
        This function handle all operations perform related to Tasks table
        """
        if splitted_operations[0] in self.available_operations:
            match splitted_operations[0]:
                case 'add':
                    self.add_operation(splitted_operations)
                case 'update':
                    self.update_operation(splitted_operations)
                case 'delete':
                    self.delete_operation(splitted_operations)
                case 'list':
                    self.list_tasks()
                case _:
                    print("\033[31m Wrong Opeeration !  \033[0m")
        else:
            print("\033[33m This Operation is not allowd !  \033[0m")


    def task_module(self):
        print("\033[34m Switching to task Module...  \033[0m")
        module_status = True
        while module_status:
            operation = self.take_user_operation('task')
            if operation == "exit":
                print("Task Module Closed")
                break
            splitted_operations = operation.split(" ")
            if operation == 'clear':
                os.system('clear')
            elif len(splitted_operations) <= 2:
                self.task_operation_handle(splitted_operations)
            else:
                print("\033[33m Cant use more than two arguments at a time !  \033[0m")


    

    def modules(self,module_name):
        if module_name == 'user':
            if self.username == 'ashishmeshram844':
                self.user_module()
            else:
                print("\033[33m You are not Authorised to access this module  \033[0m")
        elif module_name == 'task':
            self.task_module()
        


    def print_available_modules(self):
        print("\033[32m Available Modules list  \033[0m")
        table = PrettyTable()
        table.field_names = ["S.No","module name"]
        for ct,mod_nme in enumerate(self.available_modules):
            table.add_row([ct, mod_nme])
        table.max_width = 80
        table.align = 'l'
        print(table)

    def choose_module(self):
        mod_input = str(input("work@ashish : "))
        return mod_input


    def helper_commands(self,command):
        match command:
            case 'modules':
                print(self.available_modules)
                return True 
            case 'operations':
                print(self.available_operations)
                return True
            case 'clear':
                os.system('clear')
                print("work@ashish : ")
            case _:
                return False

    def main(self):
        """
        main runnner function which responsible to run programme till input exit
        """
        app_status = True 
        while app_status:
            # self.print_available_modules()
            module_input = self.choose_module()
            module_parsed = module_input.split(" ")
            # is_helper = self.helper_commands(module_parsed[0])

            if len(module_parsed) == 1:
                if module_parsed[0] == 'exit':
                    break
                elif module_parsed[0] == 'clear':
                    os.system('clear')
                elif module_parsed[0] in self.available_modules:
                    self.modules(module_parsed[0])
                else:
                    print("\033[31m Invalid Module Selected !  \033[0m")
                    print(f"\033[32m Available Modules are {self.available_modules}  \033[0m")
            else:
                print("\033[31m Inputed Module is not available !  \033[0m")
                print(f"\033[32m Available Modules are {self.available_modules}  \033[0m")

        print("Application Closed")




class Encryption(object):
    def __init__(self):
        pass

    def hash_password(self,password):
        password_bytes = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password

class Login(object):
    def __init__(self):
        self.cursor = conn.cursor()

    def check_user_avail_in_db(self,username,password):
        password = Encryption().hash_password(password)
        row = self.cursor.execute("SELECT * FROM Users WHERE (username,password) = (?,?)", (username,password)).fetchone()
        return not row is None

    def input_credentials(self):
        username = str(input("Enter Username : "))
        password = getpass.getpass(prompt="Enter password : ")
        return username,password

    def validate_credentials(self,username,password):
        if username == "ashishmeshram844" and password == "ashish@123":
            work_console = WorkConsole('ashishmeshram844')
            return work_console
        elif self.check_user_avail_in_db(username,password):
            work_console = WorkConsole(username)
            return work_console
        else:
            return None

    def login_user(self):
        username,password = self.input_credentials()
        auth_obj = self.validate_credentials(username,password)
        return auth_obj


def signal_handler(sig, frame):
    print("\033[31m \n Closed application forcefully !  \033[0m")
    sys.exit(0)

if __name__ == '__main__':
    """
    Entry point of programme
    """
    signal.signal(signal.SIGINT, signal_handler)
    try:
        login_obj = Login()
        auth = login_obj.login_user()
        if auth:
            auth.main()
        else:
            print(f"\033[31m Invalid Credentials  \033[0m")
    except Exception as e:
        print(f"\033[31m Something went wrong... \033[0m")

