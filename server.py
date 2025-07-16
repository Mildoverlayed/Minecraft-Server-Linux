import os

folder_path = os.path.join(os.path.dirname(__file__), 'Instances')
if os.path.exists(folder_path):
    directories = [entry.name for entry in os.scandir(folder_path) if entry.is_dir()]
    print(directories)
else:
    print(f"Directory '{folder_path}' does not exist.")


#java -Xmx1024M -Xms1024M -jar server.jar nogui