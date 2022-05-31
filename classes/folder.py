
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