import shutil
import os

import shutil

shutil.copy("sample.txt", "copy_sample.txt") 
shutil.copy("sample.txt", "backup_sample.txt")

file_name = "copy_sample.txt"

if os.path.exists(file_name):
    os.remove(file_name)
    print("File deleted")
else:
    print("File not found")

for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)

shutil.move("sample.txt", "folder/sample.txt")
shutil.copy("folder/sample.txt", "folder/subfolder/sample_copy.txt")
