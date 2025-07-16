#import necessary modules
import os
import json




# Functions
def ListInstances():
    """
    List all Minecraft server instances.
    """
    folder_path = os.path.join(os.path.dirname(__file__), 'Instances')
    if os.path.exists(folder_path):
        directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]
        print(directories)
    else:
        print("No instances found. Please create an instance folder in the Instances directory.")

def ClearScreen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Start of the script
ClearScreen()

with open('config.json', 'r') as openfile:

    json_object = json.load(openfile)
    print(json_object)

print("Minecraft Server Manager")
print("choose an option:")
print("1. Create Instance")
print("2. Start Instance")
print("3. Delete Instance")
print("4. Configure Instance")
print("5. Global Settings")
input_choice = int(input())

if input_choice == 1:
    # Create Instance
    ClearScreen()
    pass

elif input_choice == 2:
    # Start Instance
    ClearScreen()
    ListInstances()
    instance_name = input("Enter the instance name to start: ")
    if instance_name:
        instance_path = os.path.join(os.path.dirname(__file__), 'Instances', instance_name)
        if os.path.exists(instance_path):
            print("Use Global Max Ram amount %a (Y/N): ", Maxram )



            print(f"Starting instance: {instance_name}")


        else:
            print(f"Instance '{instance_name}' does not exist.")
    else:
        print("No instance name provided.")
    pass

elif input_choice == 3:
    # Delete Instance
    ClearScreen()
    pass

elif input_choice == 4:
    # Configure Instance
    ClearScreen()
    ListInstances()
    instance_name = input("Enter the instance name to configure: ")
    pass

elif input_choice == 5:
    # Global Settings
    ClearScreen()
    pass

else :
    print("Invalid choice. Please try again.")








#java -Xmx1024M -Xms1024M -jar server.jar nogui