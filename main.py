from classes.folder import Folder

import glob
import os
import shutil


def move_and_create_dir(source, destination):
    # Checks if directory exists and creates if not  
    if os.path.isdir(destination) == False:
        os.makedirs(destination)
        
    # Catches if file exists future implementation to change name
    try: 
        # Writes all files with the extension type to the destination  
        for files in glob.glob(source + "\*.txt"):           
            shutil.move(files, destination)
            # Writes to log file when files are moved successfully
            with open("storage/logs.txt", "a", encoding = "utf-8") as log_file:
                log_file.write(f"{files} was move to: {destination} succesfully\n")
                
    except shutil.Error:
        with open("storage/logs.txt", "a", encoding = "utf-8") as log_file:
            log_file.write(f"File already exists\n")
            
            
extension_dictionary = {"exe": {"name": "exe", "inUse": False, "group": ""}}

extension_dictionary["msi"] = {"name": "msi", "inUse": False, "group": ""}

source = "C:/Users/ikiga/Downloads/New folder"
destination = "C:/Downloads"
 
move_and_create_dir(source, destination)



"""_summary_
test cases to see if unique attribute works
"""
# john = Folder("food", "C:/Downloads")
# curb =  Folder("food", "C:/Downloads")
# if extension_dictionary["msi"]["inUse"] == False:
#     extension_dictionary["msi"]["inUse"] = True
#     extension_dictionary["msi"]["group"] = curb.name
#     curb.add_extension(extension_dictionary["msi"]["name"])
    
# if extension_dictionary["msi"]["group"] == curb.name:
#     extension_dictionary["msi"]["inUse"] = False
#     curb.remove_extension(extension_dictionary["msi"]["name"])  
    
# if extension_dictionary["msi"]["inUse"] == False:
#     extension_dictionary["msi"]["inUse"] = True
#     extension_dictionary["msi"]["group"] = john.name
#     john.add_extension(extension_dictionary["msi"]["name"])
    
# if extension_dictionary["exe"]["inUse"] == False:
#     extension_dictionary["exe"]["inUse"] = True
#     extension_dictionary["exe"]["group"] = curb.name
#     curb.add_extension(extension_dictionary["exe"]["name"])

# print(john.extension_list + curb.extension_list)