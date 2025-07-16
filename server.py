#import necessary modules
import os




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



# Start of the script
os.system('cls' if os.name == 'nt' else 'clear')

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
    pass
elif input_choice == 2:
    # Start Instance
    pass
elif input_choice == 3:
    # Delete Instance
    pass
elif input_choice == 4:
    # Configure Instance
    ListInstances()
    pass
elif input_choice == 5:
    # Global Settings
    pass
else :
    print("Invalid choice. Please try again.")








#java -Xmx1024M -Xms1024M -jar server.jar nogui