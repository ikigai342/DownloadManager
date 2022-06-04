from classes.folder import Folder
from classes.extension import Extension

import glob
import os
import shutil
import pickle

EXTENSION_NAME = "Enter extension name:\n"
FOLDER_NAME = "Enter folder name:\n"
FOLDER_DATA = "storage/FolderGroup"
EXTENSION_DATA = "storage/Extensions"

# writes text to logfile
def write_to_logfile(text):
    with open("storage/logs.txt", "a", encoding = "utf-8") as log_file:
                log_file.write(f"{text}\n")

# Moves files to directory
def move_to_directory(source, destination, extension):
    # Checks if directory exists and creates if not  
    if os.path.isdir(destination) == False:
        os.makedirs(destination)
        
    # Catches if file exists with same name 
    # Future implementation: ask user to change duplicate name
    try: 
        # Writes all files with the extension type to the destination  
        for files in glob.glob(source + f"\*.{extension}"):           
            shutil.move(files, destination)
            write_to_logfile(f"{files} was moved to: {destination} succesfully")
                
    except shutil.Error:
        write_to_logfile("File already exists")

# Adds extension to a folder class          
def add_extension(extension_dictionary, folder_dictionary):
    print(EXTENSION_NAME)
    extension_name = input()
    extension_name = extension_name.lower()
    print(FOLDER_NAME)
    folder_name = input()
    folder_name = folder_name.lower()
    if extension_dictionary[extension_name].inUse == False:
        try:
            folder_dictionary[folder_name].add_extension(extension_name)
            extension_dictionary[extension_name].inUse = True
            extension_dictionary[extension_name].group = folder_dictionary[folder_name].name
        except KeyError:
            pass
    else:
        write_to_logfile("File already in folder group")

# Removes extension to a folder class        
def remove_extension(extension_dictionary, folder_dictionary):
    print(EXTENSION_NAME)
    extension_name = input()
    extension_name = extension_name.lower()
    print(FOLDER_NAME)
    folder_name = input()
    folder_name = folder_name.lower()
    if extension_dictionary[extension_name].group == folder_name:
        try:
            folder_dictionary[folder_name].remove_extension(extension_name)
            extension_dictionary[extension_name].inUse = False
            extension_dictionary[extension_name].group = ""
        except KeyError:
            pass
    else:
        write_to_logfile("File not in folder group")

# gets folder group data from a local file
def get_folder_data():
    try:
        file = open(FOLDER_DATA, "rb")
        folder_dictionary = pickle.load(file) 
    except FileNotFoundError:    
        write_to_logfile("No Folder group data found creating empty file")
        file = open(FOLDER_DATA, "ab")
        folder_dictionary = {}
        folder_dictionary["example"] = Folder("example", "C:/Downloads/example")
        pickle.dump(folder_dictionary, file)
    finally:
        file.close()
        
    return folder_dictionary

# gets extension data from a local file    
def get_extension_data():
    try:
        file = open(EXTENSION_DATA, "rb")
        extension_dictionary = pickle.load(file)
    except FileNotFoundError: 
        write_to_logfile("No extensions data found creating empty file")
        file = open(EXTENSION_DATA, "ab")
        extension_dictionary = {}
        extension_dictionary["example"] = Extension("example")
        pickle.dump(extension_dictionary, file)
    finally:
        file.close()
        
    return extension_dictionary
    
# Saves folder and extension data to local file
def save_data(extension_dictionary, folder_dictionary):  
    file = open(EXTENSION_DATA, "wb")
    pickle.dump(extension_dictionary, file)
    file.close
    file = open(FOLDER_DATA, "wb")
    pickle.dump(folder_dictionary, file)
    file.close
    
# Finds user's download path
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')
  
extension_dictionary = get_extension_data()
folder_dictionary = get_folder_data()
source = get_download_path()

print(source)

while True:
    print("""
1. Show extension list 
2. Show folder group list
3. Create extension
4. Create folder group
5. Delete extension
6. Delete folder group
7. Add extension to folder group
8. Remove extension to folder group
9. Sort files
0. Exit
    """)
    while True:
        try:
            user_choice = int(input())
            break
        except ValueError:
            print("Please enter a valid number")
        
    match user_choice:
        # List all extensions
        case 1:
            for extensions in extension_dictionary:
                print(extension_dictionary[extensions].to_string())
        # List all folder groups
        case 2:
            for folders in folder_dictionary:
                print(folder_dictionary[folders].to_string())
        # Adds user requested extension
        case 3:
            print(EXTENSION_NAME)
            new_extension = input()
            new_extension = new_extension.lower()
            if new_extension not in extension_dictionary:
                extension_dictionary[new_extension] = Extension(new_extension)
            else:
                write_to_logfile("Extension already exists")
        # Adds user requested folder group
        case 4:
            print(FOLDER_NAME)
            new_folder_name = input()
            new_folder_name = new_folder_name.lower()
            print("Enter folder directory:\n")
            new_folder_directory = input()
            new_folder_directory = "C:/" + new_folder_directory
            if new_folder_name not in folder_dictionary:
                folder_dictionary[new_folder_name] = Folder(new_folder_name, 
                                                            new_folder_directory)
            else:
                write_to_logfile("Folder already exists")
        # Deletes user requested extension
        case 5:
            print(EXTENSION_NAME)
            delete_extension = input()
            delete_extension = delete_extension.lower()
            try:
                extension_dictionary.pop(delete_extension)
            except KeyError:
                write_to_logfile("Extension does not exists")
        # Deletes user requested folders
        case 6:
            print(FOLDER_NAME)
            delete_folder = input()
            delete_folder = delete_folder.lower()
            try:
                folder_dictionary.pop(delete_folder)
            except KeyError:
                write_to_logfile("Folder does not exists")
        # Add extension to folder group
        case 7:
            add_extension(extension_dictionary, folder_dictionary)
        # Remove extension to folder group
        case 8:       
            remove_extension(extension_dictionary, folder_dictionary)
        # Sort according folder group
        case 9:
            for folder_groups in folder_dictionary:
                for extensions in folder_dictionary[folder_groups].extension_list:
                    move_to_directory(source, folder_dictionary[folder_groups].directory
                                      , extensions)
        case 0:
            save_data(extension_dictionary, folder_dictionary)
            quit()
        case _:
            print("Not a valid input")