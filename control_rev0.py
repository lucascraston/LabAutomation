import pyvisa
import sys
import numpy as np
import matplotlib.pyplot as plt
import uuid
import pylab as pl
import webbrowser 


USB = "USB0::0xF4EC::0xEE38::SDSMMFCX5R3326::INSTR"
LAN = "TCPIP0::192.168.137.28::inst0::INSTR" # this changes with each reconnect
rm = pyvisa.ResourceManager()
adress = rm.list_resources()

scope = rm.open_resource(LAN)
print(scope.query("*IDN?"))

C1 = 'C1'
C2 = 'C2'
C3 = 'C3'
C4 = 'C4'

def volt_division(channel,voltdiv)->None:
    '''
    This sets the volt/division in volts on the specified channel
    '''
    scope.write("{}:VDIV {}V".format(channel,voltdiv))
    
def time_division(tdiv)->None:
    '''
    This will set the time/div in seconds for the entire scope
    '''
    scope.write("TDIV {}S".format(tdiv))
        
def trigger_mode(mode)->None: 
    '''
    This will set the specified trigger mode
    Options include:

    '''   
    scope.write("TRMD {}".format(mode))
    
def trigger_level(channel,level)->None:
    '''
    This sets the trigger to a specific channel and level
    '''
    scope.write("{}:TRLV {}V".format(channel,level))
    
def channel_offset(channel,offset)->None:
    '''
    This sets the offset for this channel
    '''
    scope.write("{}:OFST {}".format(channel,offset))
    
def screen_dump():
    '''
    This takes a screen shot of the scope and
    saves it as a .bmp
    '''
    scope.chunk_size = 20*1024*1024
    scope.timeout =30000
    file_name = "C:\Lucas's School\Siglent scope\Image_Folder\SCDP_{}.bmp".format(uuid.uuid4())
    scope.write("SCDP")
    result_str = scope.read_raw()
    f = open(file_name,'wb')
    f.write(result_str)
    f.flush()
    f.close()
    return file_name
        
        
def waveform_plotter(chanel):
    '''
    This will plot the current waveform in pylab
    -I aim to update it to use matplotlib
    '''
    scope.write("chdr off")
    vdiv = scope.query("{}:vdiv?".format(chanel))
    offset = scope.query("{}:ofst?".format(chanel))
    tdiv = scope.query("tdiv?")
    sample_rate = scope.query("sara?")
    sara_unit = {'Giga':1E9,'Mega':1E6,'kilo':1E3}
    for unit in sara_unit.keys():
        if sample_rate.find(unit)!=-1:
            sample_rate = sample_rate.split(unit)
            sample_rate = float(sample_rate[0])*sara_unit[unit]
            break
    sample_rate = float(sample_rate)
    scope.timeout = 30000
    scope.chunk_size = 20*1028*1028
    scope.write("{}:wf? dat2".format(chanel))
    received= list(scope.read_raw())[15:]
    received.pop()
    received.pop()
    volt_value = []
    for data in received:
        if data > 128:
            data = data - 256
        else:
            pass
        volt_value.append(data)
    time_value = []
    
    for idx in range(0,len(volt_value)):
        volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(offset)
        time_data = -(float(tdiv)*14/2)+idx*(1/sample_rate)
        time_value.append(time_data)
    pl.figure(figsize=(10,7))
    pl.plot(time_value,volt_value,markersize=1,label=u"Voltage")
    pl.legend()
    pl.grid()
    pl.show()

def web_browser()->None:
    '''
    This will open a web browser with the scopes IP
    This webpage has a GUI and you can send SCPI commands
    '''
    IP = str(scope.query("COMM_NET?").strip()).replace(",",".").replace("CONET ","")
    webbrowser.register('chrome',None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open("http://{}/welcome.php".format(IP))



dict_function = {'V':volt_division,'T':time_division,'Q':quit,'TM':trigger_mode,'TL':trigger_level,'CO':channel_offset}

measure_parameter = ['PKPK','MAX','MIN','AMPL','TOP','BASE','CMEAN','MEAN', 'STDEV','VSTD', 'RMS','CRMS','OVSN','FPRE','OVSP','RPRE', 'LEVELX','DELAY','TIMEL', 'PER', 'FREQ', 'PWID','NWID', 'RISE','FALL','WID','DUTY','NDUTY','ALL']


def get_command():
    command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")

    while command != 'Q' or command != 'q':

        if command in dict_function.keys():
            execute = dict_function.get(command)
         
        if execute == volt_division:
            chan_in,voltInput = input("Please choose your channel and Division: ").split(',')
            volt_division(chan_in,voltInput)
            command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")
            
            
        if execute == time_division:
            timeInput = input("Please choose your time Division: ")
            time_division(timeInput)
            command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")    
            
        if execute == trigger_mode:
            mode = input("choose your trigger mode; NORM, AUTO, SINGLE: ")
            trigger_mode(mode)
            command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")
            
        if execute == trigger_level:
            chan_in,level = input("choose your channel and trigger level: ").split(',')
            trigger_level(chan_in,level)
            command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")
            
        if execute == channel_offset:
            chan_in,offset = input("choose your channel and channel offset: ").split(',')
            channel_offset(chan_in,offset)
            command = input("\n V)Voltage division T)Time division TM)Trigger Mode TL)Trigger Level CO)Channel Offset Q)uit \n: ")    
        
        if execute == quit:
            quit()   
        
        
#screen_dump()        
#get_command() 
#waveform_plotter(C1) 

#web_browser()   
#volt_division(C1,0.5)  
        
       
    
    
    
    


        
        
        
        
        
        
        
        
        