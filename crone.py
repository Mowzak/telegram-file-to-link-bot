import os
import time

#crone job for deleting files

# Define the path to the folder
folder_path = os.getcwd()+"/download"
folder_path2 = os.getcwd()+"/download/premium"

# Define the time limit in seconds (1 hour = 3600 seconds)
time_limit = 3600*3

# Get the current time
current_time = time.time()
print("Salam")
# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    # Get the full path to the file
    file_path = os.path.join(folder_path, filename)
        
    # Check if the path is a file (not a directory)
    if os.path.isfile(file_path):
        # Get the file's creation time
        file_creation_time = os.path.getctime(file_path)
        
        # Calculate the file's age
        file_age = current_time - file_creation_time
        
        # Check if the file is older than the time limit
        if file_age > time_limit:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"File is not old enough to delete: {file_path}")

time_limit = 3600*12
for filename in os.listdir(folder_path2):
    # Get the full path to the file
    file_path = os.path.join(folder_path, filename)
        
    # Check if the path is a file (not a directory)
    if os.path.isfile(file_path):
        # Get the file's creation time
        file_creation_time = os.path.getctime(file_path)
        
        # Calculate the file's age
        file_age = current_time - file_creation_time
        
        # Check if the file is older than the time limit
        if file_age > time_limit:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"File is not old enough to delete: {file_path}")
