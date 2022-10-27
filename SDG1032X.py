import pyvisa
class sdg1032x:
    
    def __init__(self,adress:str):
        self.rm = pyvisa.ResourceManager()
        self.adress = adress
        self.scope = self.rm.open_resource(self.adress)