#import necessary modules
import os
import json




# Functions
def ReturnListInstances():
    """
    List all Minecraft server instances.
    """
    folder_path = os.path.join(os.path.dirname(__file__), 'Instances')
    if os.path.exists(folder_path):
        directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]
        if len(directories) > 0:
            return directories
        else:
            print("No instances found. Please create an instance folder in the Instances directory.")
            return False
    else:
        print("No instances found. Please create an instance folder in the Instances directory.")
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

# Variables
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

    print("Minecraft Server Manager")
    print("choose an option:")
    print("1. Create Instance")
    print("2. Start Instance")
    print("3. Delete Instance")
    print("4. Configure Instance")
    print("5. Global Settings")


    while True:
        try:
            input_choice = int(input())
            break
        except ValueError:
            ClearScreen()
            print("Minecraft Server Manager")
            print("choose an option:")
            print("1. Create Instance")
            print("2. Start Instance")
            print("3. Delete Instance")
            print("4. Configure Instance")
            print("5. Global Settings")
            print("\n \n Invalid input. Please enter a number.")
            continue

    if input_choice == 1:
        # Create Instance
        ClearScreen()
        pass

    elif input_choice == 2:
        # Start Instance
        ClearScreen()
        #ListInstances()
        while True:
            ClearScreen()
            instance_name = input("Enter the instance name to start: ")
            if instance_name:
                instance_path = os.path.join(os.path.dirname(__file__), 'Instances', instance_name)
                if os.path.exists(instance_path):
                    print(f"Starting instance: {instance_name}")
                    os.system(f'java -Xmx{MAXRAM}M -Xms{MINRAM}M -jar "{instance_path}/server.jar" nogui')
                    break
                else:
                    print("Instance not found. Please try again.")
            else:
                print("Instance name cannot be empty. Please try again.")

    elif input_choice == 3:
        # Delete Instance
        ClearScreen()
        if conferminput("Are you sure you want to delete an instance? (Y/n): "):
            if ReturnListInstances() != False:
                instance_name = input("Enter the instance name to delete: ")
                instance_path = os.path.join(os.path.dirname(__file__), 'Instances', instance_name)
                if os.path.exists(instance_path):
                    os.rmdir(instance_path)
                else:
                    ClearScreen()
                    print("Instance not found. Please try again. \n")

    elif input_choice == 4:
        # Configure Instance
        ClearScreen()
        pass

    elif input_choice == 5:
        # Global Settings
        ClearScreen()
        pass

    else :
        print("Invalid choice. Please try again.")








    #java -Xmx1024M -Xms1024M -jar server.jar nogui