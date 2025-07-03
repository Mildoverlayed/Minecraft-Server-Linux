from dotenv import load_dotenv
import os


load_dotenv()
os.system("ssh %s@%s" % (os.getenv("SSH_USER"), os.getenv("SSH_HOST")))
