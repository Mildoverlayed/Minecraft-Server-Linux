#import necessary modules
import os
import json
import subprocess   
import threading
import glob
from time import sleep


# Functions
def ReturnListInstances():
    global ErrorReturn
    """
    List all Minecraft server instances.
    """
    folder_path = os.path.join(os.path.dirname(__file__), 'Minecraft-Server-Linux-Submodules/Instances')
    if os.path.exists(folder_path):
        directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]
        if len(directories) > 0:
            return True, directories
        else:
            ErrorReturn = "No instances found. Please create an instance folder in the Instances directory."
            return False
    else:
        ErrorReturn = "No instances found. Please create an instance folder in the Instances directory."
        return False

def ClearScreen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def conferminput(prompt):
    """
    Get user confirmation input.
    """
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'Y' or 'n'.")

def StartScreen():
    """
    Display the start screen.
    """
    ClearScreen()
    print("Minecraft Server Manager")
    print("choose an option:")
    print("1. Create Instance")
    print("2. Start Instance")
    print("3. Delete Instance")
    print("4. Configure Instance")
    print("5. Global Settings")
    print("6. Reboot Server")
    print("7. Shutdown Server")
    print("\n \n")
    print(ErrorReturn)


def SetJavaVers(version):
    if DISTRO == "Debian GNU/Linux":
        if version in range(1.12,1.176):
            os.system("PATH=/usr/lib/jvm/zulu8-ca-arm64/jre/bin/java")
        elif version >= 1.18:
            os.system("PATH=/usr/lib/jvm/zulu17-ca-arm64/jre/bin/java")
    elif DISTRO == "Ubuntu":
        pass
    else:
        print("Unsupported distribution. Please set the Java version manually.")
        return False

def is_valid_instance_name(name):
    # Only allow alphanumeric, dash, and underscore
    return name.isidentifier() or all(c.isalnum() or c in ('-', '_') for c in name)

def StartInstance(MINRAM, MAXRAM, instance_name, instance_path):
    global ErrorReturn
    print(f"Starting instance: {instance_name}")
    print("When you are done, send /stop to stop the server. And once the screen stops moving press Ctrl + C to return to the menu.")
    sleep(1)
    jar_files = glob.glob(os.path.join(instance_path, "*.jar"))
    if not jar_files:
        ErrorReturn = "No .jar file found in the instance directory."
    else:
        jar_path = jar_files[0]  # Use the first .jar file found
        cmd = f'cd {instance_path} && java -Xmx{MAXRAM}M -Xms{MINRAM}M -jar "{jar_path}" nogui'
        proc = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1
                    )

        def read_output(p):
            for line in p.stdout:
                print(line, end='')

        output_thread = threading.Thread(target=read_output, args=(proc,))
        output_thread.daemon = True
        output_thread.start()

        try:
            while proc.poll() is None:
                user_input = input()
                if user_input.strip().lower() == "exit":
                    proc.terminate()
                    break
                proc.stdin.write(user_input + '\n')
                proc.stdin.flush()
        except KeyboardInterrupt:
            proc.terminate()
        output_thread.join()

def SetUpNgrok():
    global ErrorReturn, NGROK
    if conferminput("Are you sure you want to setup Ngrok? (Y/n): "):
        print("Setting up Ngrok...")
        ngrok_token = input("Please enter your Ngrok authtoken: from https://dashboard.ngrok.com/get-started/your-authtoken \n >>>")
        os.system(f'ngrok authtoken {ngrok_token}')
        with open('Minecraft-Server-Linux-Submodules/config.json', 'r+') as json_file:
            json_config = json.load(json_file)
            json_config['NGROK'] = True
            json_file.seek(0)
            json.dump(json_config, json_file, indent=4)
            json_file.truncate()
        NGROK= True
        ErrorReturn = "Ngrok setup complete. You can now use Ngrok to expose your server to the internet."
    else:
        ErrorReturn = "Ngrok setup cancelled."


# Variables
global ErrorReturn
ErrorReturn = ""

input_choice = 0

# Start of the script
ClearScreen()


while True:

    with open('Minecraft-Server-Linux-Submodules/config.json', 'r') as openfile:

        json_config = json.load(openfile)
        SETUP = json_config['SETUP']
        MINRAM = json_config['MINRAM']
        MAXRAM = json_config['MAXRAM']
        DISTRO = json_config['DISTRO']
        NGROK = json_config['NGROK']
        openfile.close()

    if not SETUP:
        print("Please run the setup first.")
        exit()

    StartScreen()

    while True:
        try:
            input_choice = int(input(">> "))
            break
        except ValueError:
            if not NGROK:
                ErrorReturn = "Invalid input. Please enter a number between 1 and 8."   
            else:   
                ErrorReturn = "Invalid input. Please enter a number between 1 and 7."
            ClearScreen()
            StartScreen()
            continue

    if input_choice == 1: # TODO: Create Instance
        # Create Instance
        ClearScreen()
        pass

    elif input_choice == 2:
        # Start Instance
        ClearScreen()
        bool
        if not ReturnListInstances():
            ErrorReturn = "No instances found. Please create an instance folder in the Instances directory."
            break
        print("Available instances:")
        for instance in ReturnListInstances():
            print(f" - {instance}")
        instance_name = input("Enter the instance name to start: ").strip()

        if not is_valid_instance_name(instance_name):
            ErrorReturn = "Invalid instance name. Only letters, numbers, dash, and underscore are allowed."
        else:
            try:
                base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'Minecraft-Server-Linux-Submodules/Instances'))
                instance_path = os.path.realpath(os.path.join(base_dir, instance_name))

                if not instance_path.startswith(base_dir + os.sep):
                    ErrorReturn = "Path injection detected. Aborting."
                    break
            except Exception as e:
                ErrorReturn = f"Path resolution error: {e}"
                break

            if not os.path.exists(instance_path):
                ErrorReturn = "Instance not found. Please try again."
            else:
                if instance_name not in json_config:
                    if conferminput(f"Instance '{instance_name}' does not have a Minecraft version set. Would you like to set it now? (Y/n): "):
                        minecraft_version = input("Enter the Minecraft version (e.g. 1.16.5): ")
                        json_config[instance_name] = {
                            "version": minecraft_version
                        }
                        with open('Minecraft-Server-Linux-Submodules/config.json', 'w') as json_file:
                            json.dump(json_config, json_file, indent=4)

                # Handle EULA
                eula_path = os.path.join(instance_path, 'eula.txt')
                if os.path.exists(eula_path):
                    sleep(1)
                    with open(eula_path, "r") as file:
                        data = file.read()
                        if "eula=false" in data:
                            data = data.replace("eula=false", "eula=true")
                            with open(eula_path, "w") as file:
                                file.write(data)
                                sleep(1)
                    os.system(f'echo "eula=true" > {eula_path}')
                else:
                    sleep(1)
                    with open(eula_path, 'w') as f:
                        f.write('eula=true\n')
                        f.close()
                    print("eula.txt created and set to eula=true.")
                    sleep(1)
                if NGROK:
                    if conferminput("Would you like to use Ngrok to expose your server to the internet? (Y/n): "):
                        print("Starting Ngrok...")
                        os.system('ngrok tcp 25565 ')
                        sleep(1)
                        print("Ngrok started. You can find the public address in the terminal output.")

                StartInstance(MINRAM, MAXRAM, instance_name, instance_path)

    elif input_choice == 3: 
        # Delete Instance
        ClearScreen()
        if conferminput("Are you sure you want to delete an instance? (Y/n): "):
            statement, directories = ReturnListInstances().split()
            if statement:
                print("Available instances:")
                for instance in directories:
                    print(f" - {instance}")
                instance_name = input("Enter the instance name to delete: ")
                instance_path = os.path.join(os.path.dirname(__file__), 'Instances', instance_name)
                if os.path.exists(instance_path):
                    if conferminput(f"Are you sure you want to delete the instance '{instance_name}'? (Y/n): "):
                        os.system(f'rm -rf "{instance_path}"')
                        with open('config.json', 'r+') as json_file:
                            json_config = json.load(json_file)
                            if instance_name in json_config:
                                del json_config[instance_name]
                                json_file.seek(0)
                                json.dump(json_config, json_file, indent=4)
                                json_file.truncate()
                        ErrorReturn = f"Instance '{instance_name}' deleted successfully."
                    else:
                        ErrorReturn = "Deletion cancelled."
                else:
                    ErrorReturn = "Instance not found. Please try again."
        else:
            ErrorReturn = "Deletion cancelled."

    elif input_choice == 4: # TODO: Configure Instance
        ClearScreen()
        pass

    elif input_choice == 5: # TODO: Global Settings
        while True:
            print("Current Config")
            print(f"""Minimum RAM: {MINRAM}MB \n
                  Maximum RAM: {MAXRAM}MB \n
                  Distro: {DISTRO} \n
                  Ngrok Enabled: {NGROK}
                """)
            if conferminput("Would you like to change a setting? (Y/n): "):
                ClearScreen()
                print("1. Change Minimum RAM")
                print("2. Change Maximum RAM")
                print("3. Change Distro")
                print("4. Toggle Ngrok")
                print("5. Back to Main Menu")
                while True:
                    try:
                        setting_choice = int(input(">> "))
                        break
                    except ValueError:
                        ErrorReturn = "Invalid input. Please enter a number between 1 and 5."
                        ClearScreen()
                        StartScreen()
                        continue

                if setting_choice == 1:
                    new_min_ram = input("Enter new Minimum RAM in MB: ")
                    json_config['MINRAM'] = int(new_min_ram)
                    with open('Minecraft-Server-Linux-Submodules/config.json', 'w') as json_file:
                        json.dump(json_config, json_file, indent=4)
                    ErrorReturn = f"Minimum RAM set to {new_min_ram}MB."

                elif setting_choice == 2:
                    new_max_ram = input("Enter new Maximum RAM in MB: ")
                    json_config['MAXRAM'] = int(new_max_ram)
                    with open('Minecraft-Server-Linux-Submodules/config.json', 'w') as json_file:
                        json.dump(json_config, json_file, indent=4)
                    ErrorReturn = f"Maximum RAM set to {new_max_ram}MB."

                elif setting_choice == 3:
                    new_distro = input("Enter new Distro (Debian GNU/Linux or Ubuntu): ")
                    if new_distro in ["Debian GNU/Linux", "Ubuntu"]:
                        json_config['DISTRO'] = new_distro
                        with open('Minecraft-Server-Linux-Submodules/config.json', 'w') as json_file:
                            json.dump(json_config, json_file, indent=4)
                        ErrorReturn = f"Distro set to {new_distro}."
                    else:
                        ErrorReturn = "Invalid Distro. Please try again."

                elif setting_choice == 4:
                    if NGROK:
                        NGROK = False
                        json_config['NGROK'] = False
                        with open('Minecraft-Server-Linux-Submodules/config.json', 'w') as json_file:
                            json.dump(json_config, json_file, indent=4)
                        ErrorReturn = "Ngrok disabled."
                    else:
                        SetUpNgrok()
                        ErrorReturn = "Ngrok enabled."
                elif setting_choice == 5:
                    ClearScreen()
                    break
            
    
    elif input_choice == 6: # Exit
        ClearScreen()
        print("rebooting the server...")
        os.system('sudo reboot now')

    elif input_choice == 7: # TODO: Shutdown Server
        ClearScreen()
        if conferminput("Are you sure you want to shutdown the server? (Y/n): "):
            print("Shutting down the server...")
            os.system('sudo shutdown now')
        else:
            ErrorReturn = "Shutdown cancelled."










    #java -Xmx1024M -Xms1024M -jar server.jar nogui