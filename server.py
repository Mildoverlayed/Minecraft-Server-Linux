#import necessary modules
import os
import json
import subprocess   
import sys
import threading
import glob
from time import sleep
from datetime import datetime
import pytz


# Functions
def ReturnListInstances():
    global ErrorReturn
    """
    List all Minecraft server instances.
    """
    folder_path = os.path.join(os.path.dirname(__file__), 'Instances')
    if os.path.exists(folder_path):
        directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]
        if len(directories) > 0:
            return directories
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

def get_eula_time():
    # Set the Eastern Timezone
    zone = pytz.timezone(ZONE)

    # Get current UTC time and convert it to Eastern Time
    now = datetime.now(pytz.utc).astimezone(zone)

    # Format it to match the desired style
    formatted = now.strftime('%a %b %d %H:%M:%S %Z %Y')
    return formatted

# Variables
global ErrorReturn
ErrorReturn = ""

input_choice = 0

# Start of the script
ClearScreen()
while True:

    with open('config.json', 'r') as openfile:

        json_config = json.load(openfile)
        SETUP = json_config['SETUP']
        MINRAM = json_config['MINRAM']
        MAXRAM = json_config['MAXRAM']
        DISTRO = json_config['DISTRO']
        ZONE = json_config['ZONE']

    if not SETUP:
        print("Please run the setup first.")
        exit()

    StartScreen()

    while True:
        try:
            input_choice = int(input(">> "))
            break
        except ValueError:
            ErrorReturn = "Invalid input. Please enter a number between 1 and 5."
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
        if ReturnListInstances() == False:
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
                base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'Instances'))
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
                        with open('config.json', 'w') as json_file:
                            json.dump(json_config, json_file, indent=4)

                # Handle EULA
                
                eula_path = os.path.join(instance_path, 'eula.txt')
                if os.path.exists(eula_path):
                    with open(eula_path, 'r') as f:
                        lines = f.readlines()
                    updated = False
                    for i, line in enumerate(lines):
                        if line.strip() == 'eula=false':
                            lines[i] = 'eula=true\n'
                            updated = True
                    if updated:
                        with open(eula_path, 'w') as f:
                            f.writelines(lines)
                            f.close()
                        print("eula.txt updated to eula=true.")
                    else:
                        print("eula.txt already set to true. No changes made.")
                else:
                    with open(eula_path, 'w') as f:
                        f.write(get_eula_time() + '\n')
                        f.write('eula=true\n')
                        f.close()
                    print("eula.txt created and set to eula=true.")
                with open(eula_path, 'r+') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if i == 1:
                            lines[i] = get_eula_time() + '\n'
                            break
                    f.writelines(lines)
                    f.close()
                print("eula.txt Time updated.")
                sleep(1)

                print(f"Starting instance: {instance_name}")
                jar_files = glob.glob(os.path.join(instance_path, "*.jar"))
                if not jar_files:
                    ErrorReturn = "No .jar file found in the instance directory."
                else:
                    jar_path = jar_files[0]  # Use the first .jar file found
                    cmd = f'java -Xmx{MAXRAM}M -Xms{MINRAM}M -jar "{jar_path}" nogui'
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

    elif input_choice == 3: 
        # Delete Instance
        ClearScreen()
        if conferminput("Are you sure you want to delete an instance? (Y/n): "):
            if ReturnListInstances() != False:
                print("Available instances:")
                for instance in ReturnListInstances():
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
        # Global Settings
        pass
    
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

    else :
        print("Invalid choice. Please try again.")








    #java -Xmx1024M -Xms1024M -jar server.jar nogui