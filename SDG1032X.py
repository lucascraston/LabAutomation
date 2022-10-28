import pyvisa
import binascii
import time
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

    def arb_serial_uart(self):
        '''
        our arb uses little endian, 2s complement
        we also have a 14 bit AWG, therefor we can have [-8192:8192]
        we will go from 0 to 8192 (low to high) or visa versa
        8191 = 0x2000 -> 2s compliment little endian
        0 = 0x0000
        '''

        wave_points = [0x0000, 0x2000]
        '''
        wave_points = []
        
        
        for i in range(0,16384):
            if(i<=8192):
                wave_points.append(wave_data[0])
            else:
                wave_points.append(wave_data[1])  

        #wave_points = [0xe000, 0xe000, 0xf000, 0xf000, 0x0000, 0x0000, 0x1000, 0x1000, 0x2000, 0x2000]
        '''   
        
        f = open("wave1.bin", "wb")
        for  i in wave_points:
            b = hex(i)
            b=b[2:]
            len_b = len(b)
            if(0==len_b):
                b = '0000'
            elif(1== len_b):
                b = '000' +b
            elif(2== len_b):
                b = '00' +b
            elif(3  ==len_b):
                b = '0' +b            
            b = b[2:4] + b[:2]
            c = binascii.unhexlify(b)
            f.write(c)
        f.close()    
        #return 1    

    def send_wave_data(self):
        """send wave1.bin to the device"""
        f = open("wave1.bin", "rb")    #wave1.bin is the waveform to be sent
        data = f.read().decode("latin1")
        print('write class:', type(data))
        print('write bytes:',len(data))
        self.awg.write_termination = ''
        self.awg.write("C1:WVDT WVNM,wave1,FREQ,2000.0,AMPL,2.0,OFST,0.0,PHASE,0.0,WAVEDATA,%s"%(data),encoding='latin1')    #"X" series (SDG1000X/SDG2000X/SDG6000X/X-E)&amp;amp;amp;lt;/pre&amp;amp;amp;gt;
        self.awg.write("C1:ARWV NAME,wave1")
        f.close()
        return data    


    def get_wave_data(self):
        """get wave from the devide"""
        f = open("wave2.bin", "wb")
        
         #save the waveform as wave2.bin
        self.awg.write("WVDT? user,wave1")
         #"X" series (SDG1000X/SDG2000X/SDG6000X/X-E)
        time.sleep(1)
        data = self.awg.read()
        data_pos = data.find(("WAVEDATA,") + len("WAVEDATA,"))
        #print(data[0:data_pos])
        wave_data = data[data_pos:]
        #print('read bytes:',len(wave_data))
        f.write(wave_data)
        f.close()    


awg = sdg1032x("TCPIP0::10.42.0.107::inst0::INSTR")
print("connection initiaded")
#awg.channel_output("C1","ON","50")    
awg.arb_serial_uart()
send = awg.send_wave_data()
#wg.get_wave_data()

