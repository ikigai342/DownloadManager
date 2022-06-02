from importlib.util import source_hash
from classes.folder import Folder
from classes.extension import Extension

import glob
import os
import shutil
import pickle

# writes text to logfile
def write_to_logfile(text):
    with open("storage/logs.txt", "a", encoding = "utf-8") as log_file:
                log_file.write(f"{text}\n")

# Moves files to library
def move_and_create_dir(source, destination, extension):
    # Checks if directory exists and creates if not  
    if os.path.isdir(destination) == False:
        os.makedirs(destination)
        
    # Catches if file exists future implementation to change name
    try: 
        # Writes all files with the extension type to the destination  
        for files in glob.glob(source + f"\*.{extension}"):           
            shutil.move(files, destination)
            write_to_logfile(f"{files} was move to: {destination} succesfully")
                
    except shutil.Error:
        write_to_logfile("File already exists")

# Adds extension to a folder class          
def add_extension(extension_dictionary, folder_dictionary):
    print("Enter extension name:\n")
    extension_name = input()
    extension_name = extension_name.lower()
    print("Enter folder name:\n")
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
    print("Enter extension name:\n")
    extension_name = input()
    extension_name = extension_name.lower()
    print("Enter folder name:\n")
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

# Loads folder group data from file
def load_folder_data():
    try:
        file = open("storage/FolderGroup", "rb")
        folder_dictionary = pickle.load(file) 
    except FileNotFoundError:    
        write_to_logfile("No Folder group data found creating empty file")
        file = open("storage/FolderGroup", "ab")
        folder_dictionary = {}
        folder_dictionary["example"] = Folder("example", "C:/Downloads/example")
        pickle.dump(folder_dictionary, file)
    finally:
        file.close()
        return folder_dictionary

# Loads folder group data from file    
def load_extension_data():
    try:
        file = open("storage/Extensions", "rb")
        extension_dictionary = pickle.load(file)
    except: 
        write_to_logfile("No extensions data found creating empty file")
        file = open("storage/Extensions", "ab")
        extension_dictionary = {}
        extension_dictionary["example"] = Extension("example")
        pickle.dump(extension_dictionary, file)
    finally:
        file.close()
        return extension_dictionary
def save_data(extension_dictionary, folder_dictionary):  
    file = open("storage/Extensions", "wb")
    pickle.dump(extension_dictionary, file)
    file.close
    file = open("storage/FolderGroup", "wb")
    pickle.dump(folder_dictionary, file)
    file.close
    
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
  
extension_dictionary = load_extension_data()
folder_dictionary = load_folder_data()
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
            print("Enter extension name:\n")
            new_extension = input()
            new_extension = new_extension.lower()
            if new_extension not in extension_dictionary:
                extension_dictionary[new_extension] = Extension(new_extension)
            else:
                write_to_logfile("Extension already exists")
        # Adds user requested folder group
        case 4:
            print("Enter folder name:\n")
            new_folder_name = input()
            new_folder_name = new_folder_name.lower()
            print("Enter folder directory:\n")
            new_folder_dir = input()
            new_folder_dir = "C:/" + new_folder_dir
            if new_folder_name not in folder_dictionary:
                folder_dictionary[new_folder_name] = Folder(new_folder_name, new_folder_dir)
            else:
                write_to_logfile("Folder already exists")
        # Deletes user requested extension
        case 5:
            print("Enter extension name:\n")
            delete_extension = input()
            delete_extension = delete_extension.lower()
            try:
                extension_dictionary.pop(delete_extension)
            except KeyError:
                write_to_logfile("Extension does not exists")
        # Deletes user requested folders
        case 6:
            print("Enter extension name:\n")
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
                    move_and_create_dir(source, folder_dictionary[folder_groups].directory, extensions)
        case 0:
            save_data(extension_dictionary, folder_dictionary)
            quit()
        case _:
            print("Not a valid input")
    
