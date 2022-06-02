from unicodedata import name


class Folder:
    def __init__(self, name, directory):
        self.name = name
        self.extension_list = []
        self.directory = directory
    
    def add_extension(self, abbreviaton):
        self.extension_list.append(abbreviaton)
        pass
    
    def remove_extension(self, abbreviaton):
        self.extension_list.remove(abbreviaton)
        pass
    
    # Returns string with folder data
    def to_string(self):
        temp_string = f"Folder group\n name: {self.name}\n dir: {self.directory}\n"
        for extension in self.extension_list:
            temp_string += f" extension: {extension}\n"
        
        return temp_string