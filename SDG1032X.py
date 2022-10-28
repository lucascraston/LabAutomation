import pyvisa
class sdg1032x:
    
    def __init__(self,adress:str):
        self.rm = pyvisa.ResourceManager()
        self.adress = adress
        self.awg = self.rm.open_resource(self.adress)


    def channel_output(self,channel:str,state:str,impedance:str):
        '''
        channel: 'C1' or 'C2'
        state: 'ON' or 'OFF'
        impedance: 'HZ' or '50'
        
        '''
        self.awg.write("{}:OUTP {},LOAD,{},PLRT,NOR".format(channel,state,impedance))

    def arb_serial(self):
        return 1    


awg = sdg1032x("TCPIP0::10.42.0.107::inst0::INSTR")
print("connection initiaded")
awg.channel_output("C1","ON","50")    