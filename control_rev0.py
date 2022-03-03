import pyvisa
import sys
import numpy as np
import matplotlib.pyplot as plt
import uuid

USB = "USB0::0xF4EC::0xEE38::SDSMMFCX5R3326::INSTR"
LAN = "TCPIP0::192.168.137.203::inst0::INSTR" # this changes with each reconnect

rm = pyvisa.ResourceManager()
adress = rm.list_resources()

scope = rm.open_resource(LAN)
print(scope.query("*IDN?"))



def volt_division(channel,voltdiv):
    scope.write("{}:VDIV {}V".format(channel,voltdiv))
    
def time_division(tdiv):
        scope.write("TDIV {}S".format(tdiv))
        
def trigger_mode(mode):    
    scope.write("TRMD {}".format(mode))
    
def trigger_level(channel,level):
    scope.write("{}:TRLV {}V".format(channel,level))
    
def channel_offset(channel,offset):
    scope.write("{}:OFST {}".format(channel,offset))\
    
def screen_dump():
        scope.chunk_size = 20*1024*1024
        scope.timeout =30000
        file_name = "C:\Lucas's School\Siglent scope\SCDP_{}.bmp".format(uuid.uuid4())
        scope.write("SCDP")
        result_str = scope.read_raw()
        f = open(file_name,'wb')
        f.write(result_str)
        f.flush()
        f.close()
        
        
#def waveform_plotter():
        


C1 = 'C1'
C2 = 'C2'
C3 = 'C3'
C4 = 'C4'

  
#function_list = ['M','V','T','TM','TL','Q']

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
        
        
screen_dump()        
get_command()        
        
       
    
    
    
    


        
        
        
        
        
        
        
        
        