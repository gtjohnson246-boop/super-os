import os
import sys
import webbrowser
import platform
import getpass
from datetime import datetime

# Set up global credentials
VALID_USERNAME = "gabeee"
VALID_PASSWORD = "6655"

def show_boot_screen():
    """Displays a stylized OS boot screen with system information."""
    print("=" * 55)
    print(r"  __  __ _       _        ____   ____  ")
    print(r" |  \/  (_)_ __ (_)      / __ \ / ___| ")
    print(r" | |\/| | | '_ \| |_____| |  | |\___ \ ")
    print(r" | |  | | | | | | |_____| |__| | ___) |")
    print(r" |_|  |_|_|_| |_|_|      \____/ |____/ ")
    print("=" * 55)
    print(f" Mini-Python-OS Version: 1.8.0")
    print(f" Host Machine Kernel : {platform.system()} {platform.release()}")
    print(f" System Time         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)
    print(" Boot Sequence Completed successfully.")
    print("=" * 55 + "\n")

def show_lockout_screen():
    """Displays your compact ASCII art followed by the lockout notice."""
    tux_art = [
        "##########**************************##########",
        "######***************%%%%%**************######",
        "###*****************#%%%#@@****************###",
        "##****************+++==+=%@*****************##",
        "#*********++++++++++*=--=%@#*+++++++*********#",
        "********++++++++++*%#::::+%%#*++++++++********",
        "******+++++++++++*%#:....+%%@#++++++++++******",
        "********+++++++++*%=::..=%%%@%++++++++********",
        "#*********++++++=*@#::::*%%%#@++++++*********#",
        "##*************+====+===+*+==*+*************##",
        "####*************++++@@@#++++++***********####",
        "######**************#%@@%++**#**********######",
        "##########**************************##########"
    ]
    
    print("\n" + "!" * 46)
    print(" " * 14 + "SYSTEM LOCKED!")
    print(" " * 7 + "Too many failed login attempts.")
    print(" " * 11 + "PLEASE CONTACT OWNER.")
    print("!" * 46 + "\n")
    
    # Print the exact compact 46-character wide ASCII pattern
    for line in tux_art:
        print(line)
    print()

def authenticate_user():
    """Prompts user for credentials and returns True if correct. Locks out after 5 attempts."""
    print("--- SYSTEM AUTHENTICATION REQUIRED ---")
    
    attempts = 5
    while attempts > 0:
        username = input("Username: ").strip()
        # Note: On some online web compilers like OneCompiler, getpass might echo text 
        # normally due to browser terminal limits, but it functions properly.
        password = getpass.getpass("Password: ").strip()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            print("\nAccess Granted. Welcome back, Gabeee!\n")
            return True
        else:
            attempts -= 1
            print(f"\n[!] Invalid credentials. Access Denied.")
            if attempts > 0:
                print(f"You have {attempts} attempt(s) remaining.\n")
            else:
                show_lockout_screen()
                sys.exit()

def run_mini_os():
    show_boot_screen()
    authenticate_user()

    print("Type 'help' for available commands or 'exit' to quit.\n")

    while True:
        try:
            cwd = os.getcwd()
            command_line = input(f"mini-os:{cwd}> ").strip()
            
            if not command_line:
                continue

            parts = command_line.split()
            cmd = parts[0].lower()  # Fixed list element mapping bug from previous version
            args = parts[1:] if len(parts) > 1 else []

            if cmd == "exit":
                print("Shutting down Mini-Python-OS. Goodbye!")
                break

            elif cmd == "help":
                print("Available commands:")
                print("  help           - Show this help message")
                print("  pwd            - Print current working directory")
                print("  ls             - List files and folders")
                print("  cd <dir>       - Change directory")
                print("  mkdir <name>   - Create a new directory")
                print("  cat <file>     - Read and display a text file")
                print("  search_engine  - Open Google in your web browser")
                print("  open_downloads - Pull up your Chromebook's system file manager")
                print("  clear          - Clear the starting screen / terminal screen")
                print("  exit           - Exit the mini OS shell")

            elif cmd == "pwd":
                print(os.getcwd())

            elif cmd == "ls":
                items = os.listdir(os.getcwd())
                for item in items:
                    print("  ", item)

            elif cmd == "cd":
                if not args:
                    print("Error: 'cd' requires a path argument.")
                else:
                    path = " ".join(args)
                    try:
                        os.chdir(path)
                    except OSError as e:
                        print(f"Error: {e}")

            elif cmd == "mkdir":
                if not args:
                    print("Error: 'mkdir' requires a directory name.")
                else:
                    folder_name = " ".join(args)
                    try:
                        os.mkdir(folder_name)
                        print(f"Directory '{folder_name}' created.")
                    except OSError as e:
                        print(f"Error: {e}")

            elif cmd == "cat":
                if not args:
                    print("Error: 'cat' requires a file name.")
                else:
                    file_path = " ".join(args)
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                print(f.read())
                        except Exception as e:
                            print(f"Error reading file: {e}")
                    else:
                        print(f"Error: File '{file_path}' not found.")

            elif cmd == "search_engine":
                print("Opening Google in your web browser...")
                webbrowser.open("https://google.com")

            elif cmd == "open_downloads":
                print("Opening your Chromebook's file manager...")
                # Workaround protocol used to summon native file interfaces from inside the browser tab
                webbrowser.open("chrome://file-manager")

            elif cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for a list of commands.")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit properly.")
        except EOFError:
            break

if __name__ == "__main__":
    run_mini_os()


