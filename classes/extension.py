class Extension:
    def __init__(self, name):
        self.name = name
        self.inUse = False
        self.group = ""
    
    # Returns string with extension data
    def to_string(self):
        temp_string =  f"Extension\n name: {self.name}\n In use: {self.inUse}\n " 
        temp_string += f"group: {self.group}\n"
        return temp_string