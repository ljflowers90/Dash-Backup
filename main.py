import os
from dotenv import load_dotenv
import paramiko
import stat

# Load .env file
load_dotenv()

# Get credentials from .env
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.0.205', username=username, password=password)

# Initialize SFTP client
sftp = ssh.open_sftp()

# Get list of files in /mnt/dash/captures/ sorted by modification time
files = sftp.listdir_attr('/mnt/dash/captures/')
files.sort(key=lambda x: x.st_mtime)

# Get the latest file
latest_file = files[-1]

# Transfer file to local machine
sftp.get(f'/mnt/dash/captures/{latest_file.filename}', f'./{latest_file.filename}')

# Delete source file
sftp.remove(f'/mnt/dash/captures/{latest_file.filename}')

# Close connections
sftp.close()
ssh.close()