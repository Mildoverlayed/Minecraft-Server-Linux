#import necessary modules
import os
import json
import subprocess   
import sys
import threading
import glob
import time
import zipfile

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


# Variables
global ErrorReturn
ErrorReturn = ""

input_choice = 0

# Start of the script
ClearScreen()
while True:

    with open('config.json', 'r') as openfile:

        json_object = json.load(openfile)
        SETUP = json_object['SETUP']
        MINRAM = json_object['MINRAM']
        MAXRAM = json_object['MAXRAM']

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
        instance_name = input("Enter the instance name to start: ")
        if instance_name:
            instance_path = os.path.join(os.path.dirname(__file__), 'Instances', instance_name)
            if os.path.exists(instance_path):
                print(f"Starting instance: {instance_name}")
                jar_files = glob.glob(os.path.join(instance_path, "*.jar"))
                if not jar_files:
                    ErrorReturn = "No .jar file found in the instance directory."
                else:
                    jar_path = jar_files[0]  # Use the first .jar file found
                    with zipfile.ZipFile(jar_path) as jar:
                        with jar.open('META-INF/MANIFEST.MF') as manifest:
                            for line in manifest:
                                decoded = line.decode().strip()
                                if 'Implementation-Version' in decoded:
                                    print("Minecraft server version:", decoded.split(":")[-1].strip())
                                    break
                    time.sleep(10)  # Wait for the version to be read









                    """
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
                    """
            else:
                ErrorReturn = "Instance not found. Please try again."
        else:
            ErrorReturn = "Instance name cannot be empty. Please try again."

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