
import pyvisa
import uuid

class sds1104xe:

    def __init__(self,adress:str):
        self.rm = pyvisa.ResourceManager()
        self.adress = adress
        self.scope = self.rm.open_resource(self.adress)

    def volt_division(self,channel,voltdiv)->None:
        '''
        This sets the volt/division in volts on the specified channel
        '''
        self.scope.write("{}:VDIV {}V".format(channel,voltdiv))
    def time_division(self,tdiv)->None:
        '''
        This will set the time/div in seconds for the entire scope
        '''
        self.scope.write("TDIV {}S".format(tdiv))
        
    def trigger_mode(self,mode)->None: 
        '''
        This will set the specified trigger mode
        Options include:

        '''   
        self.scope.write("TRMD {}".format(mode))
    
    def trigger_level(self,channel,level)->None:
        '''
        This sets the trigger to a specific channel and level
        '''
        self.scope.write("{}:TRLV {}V".format(channel,level))

    def channel_offset(self,channel,offset)->None:
        '''
        This sets the offset for this channel
        '''
        self.scope.write("{}:OFST {}".format(channel,offset))

    def screen_dump(self)->str:
        '''
        This takes a screen shot of the scope and
        saves it as a .bmp
        '''
        self.scope.chunk_size = 20*1024*1024
        self.scope.timeout =30000
        file_name = "C:\Lucas's School\Siglent scope\Image_Folder\SCDP_{}.bmp".format(uuid.uuid4())
        self.scope.write("SCDP")
        result_str = self.scope.read_raw()
        f = open(file_name,'wb')
        f.write(result_str)
        f.flush()
        f.close()
        return file_name

    



scope = sds1104xe("TCPIP0::10.42.0.133::inst0::INSTR")
print("connection initiaded")
scope.volt_division("C1",0.5)