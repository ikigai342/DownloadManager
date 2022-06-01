from distutils import extension
from classes.folder import Folder

import glob
import os
import shutil
import pickle

# writes text to logfile
def write_to_logfile(text):
    with open("storage/logs.txt", "a", encoding = "utf-8") as log_file:
                log_file.write(f"{text}\n")

# Moves files to library
def move_and_create_dir(source, destination):
    # Checks if directory exists and creates if not  
    if os.path.isdir(destination) == False:
        os.makedirs(destination)
        
    # Catches if file exists future implementation to change name
    try: 
        # Writes all files with the extension type to the destination  
        for files in glob.glob(source + "\*.txt"):           
            shutil.move(files, destination)
            write_to_logfile(f"{files} was move to: {destination} succesfully\n")
                
    except shutil.Error:
        write_to_logfile(f"File already exists\n")

# Adds extension to a folder class          
def add_extension(extension_dictionary, folder, extension_name):
    if extension_dictionary[extension_name]["inUse"] == False:
        extension_dictionary[extension_name]["inUse"] = True
        extension_dictionary[extension_name]["group"] = folder.name
        folder.add_extension(extension_dictionary[extension_name]["name"])

# Removes extension to a folder class        
def remove_extension(extension_dictionary, folder, extension_name):
    if extension_dictionary[extension_name]["group"] == folder.name:
        extension_dictionary[extension_name]["inUse"] = False
        extension_dictionary[extension_name]["group"] = ""
        folder.remove_extension(extension_dictionary[extension_name]["name"])

# Loads folder group data from file
def load_folder_data():
    try:
        file = open("storage/FolderGroup", "rb")
        folder_list = pickle.load(file) 
    except FileNotFoundError:    
        write_to_logfile("No Folder group data found creating empty file")
        file = open("storage/FolderGroup", "ab")
        folder_list = []
        folder_list.append(Folder("Example", "C:/Downloads/Example"))
        pickle.dump(folder_list, file)
    finally:
        file.close()
        return folder_list

# Loads folder group data from file    
def load_extension_data():
    try:
        file = open("storage/Extensions", "rb")
        extension_dictionary = pickle.load(file)
    except: 
        write_to_logfile("No extensions data found creating empty file")
        file = open("storage/Extensions", "ab")
        extension_dictionary = {}
        extension_dictionary["example"] = {"name": "example", "inUse": False, 
                                        "group": ""}
        pickle.dump(extension_dictionary, file)
    finally:
        file.close()
        return extension_dictionary
        
  
extension_dictionary = load_extension_data()
folder_list = load_folder_data()


while True:
    print("""
1. Show extension list 
2. Show folder group list
3. Create extension
4. Remove extension
5. Create folder group
6. Remove folder group
7. Add extension to folder group
0. Exit
    """)
    try:
        match int(input()):
            case 1:
                for extensions in extension_dictionary:
                    print(extensions)
            case 2:
                for folders in folder_list:
                    print(folders.name)
            case 3:
                print("Enter extension name:\n")
                new_extension = input()
                extension_dictionary[new_extension] = {"name": new_extension, 
                                                       "inUse": False, 
                                                        "group": ""}
            case 4:
                print("Enter extension name:\n")
                delete_extension = input()
                extension_dictionary.pop(delete_extension)
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case 0:
                quit()
            case _:
                print("Not a valid input")
    except ValueError:
        print("Please enter a valid number")
