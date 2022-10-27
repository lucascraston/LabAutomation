import pyvisa
import sys
import numpy as np
import matplotlib.pyplot as plt
import uuid
import pylab as pl
import webbrowser 
import PySimpleGUI as pg
from PIL import Image
import io
import time


USB = "USB0::0xF4EC::0xEE38::SDSMMFCX5R3326::INSTR" # USB Pyvisa resource number
LAN = "TCPIP0::10.42.0.133::inst0::INSTR" # this changes with each reconnect
rm = pyvisa.ResourceManager()
adress = rm.list_resources()

pg.theme("Darkteal2")

scope = rm.open_resource(LAN) #connect to the scope
print(scope.query("*IDN?")) #print the device ID

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
    
def screen_dump()->str:
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
        
        
def waveform_plotter(chanel)->None:
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

def end_session()->None:

    scope.close()

def command():
    '''
    Generic SCPI write command for our terminal
    '''
    scope.write(values["SCPI Command"])


def measure_all(channel):
    '''
    reads all measurements for the channel
    and returns it as a list of lists 
    '''
    data = (scope.query("{}:PAVA? ALL".format(channel))).replace("{}:PAVA ".format(channel),"")
    
    data =  data.split(",")
    
    measure_data = {data[i]:data[i+1] for i in range(0,len(data),2)}
    data_array=[]
    for key in measure_data:
        
        data_info=[key,measure_data[key]]
        data_array.append(data_info)
    return data_array


    
    

measure_parameter = [
    ["PKPK","1","",""],
    ['MAX',"2","",""],
    ['MIN',"3","",""],
    ['AMPL',"4","",""],
    ['TOP',"","",""],
    ['BASE',"","",""],
    ['CMEAN',"","",""],
    ['MEAN',"","",""],
    ['STDEV',"","",""],
    ['VSTD',"","",""],
    ['RMS',"","",""],
    ['CRMS',"","",""],
    ['OVSN',"","",""],
    ['FPRE',"","",""],
    ['OVSP',"","",""],
    ['RPRE',"","",""],
    ['LEVELX',"","",""],
    ['DELAY',"","",""],
    ['TIMEL',"","",""],
    ['PER',"","",""],
    ['FREQ',"","",""],
    ['PWID',"","",""],
    ['NWID',"","",""],
    ['RISE',"","",""],
    ['FALL',"","",""],
    ['WID',"","",""],
    ['DUTY',"","",""],
    ['NDUTY',"","",""],
    ['ALL',"","",""]
    ]

headings=["Measure","Source"]



def update_image():
    '''
    Updates our window immage by calling our Screen dump
    function and converting it to PNG 
    We call this after every event so we need to 
    sleep so we ensure the scopes display is updated
    '''
    time.sleep(0.75) 
    file_name = screen_dump()
    image = Image.open(file_name)
    bio= io.BytesIO()
    image.save(bio,format = "PNG")
    window["Image"].update(data=bio.getvalue())

#table for the measurements
measurement_table_column=[
    [pg.Checkbox("C1",key="checkC1"),pg.Checkbox("C2",key="checkC2"),pg.Checkbox("C3",key="checkC3"),pg.Checkbox("C4",key="checkC4")],
    [pg.Table(values=measure_all(C1),num_rows= len(measure_parameter),headings=headings,auto_size_columns=True,key="Table")]
]    
#column for the generic scope functions
function_column = [

    [pg.Text("SCPI Terminal:"),pg.InputText(key="SCPI Command",size = (20,1)),pg.Button("Go"),pg.Button("Clear")],
    #[pg.Output(size = (75,5),key = "Output")],
    [pg.Text("Input Voltage Values(V):"),pg.InputText(key="VDIV",size=(15,1)),pg.Text("Input Time Values(S):"),pg.InputText(key="TDIV",size=(15,1))],
    
    #[pg.Text("Image Folder:"),pg.In(size=(20,1),enable_events=True,key="Folder"),pg.FolderBrowse()],
    [pg.Text("Select your channel:"),pg.Combo(["C1","C2","C3","C4"]),pg.Text("Select the trigger mode:"),pg.Combo(["AUTO","NORM","SINGLE","STOP"])],
    [pg.Button("Voltage Division",tooltip = "Channel,Volt/Div"),
    pg.Button("Time Division",tooltip = "Time/Div"),pg.Button("Web Page"),pg.Button("Screen Dump"),pg.Button("Trigger Mode")],
    [pg.Button("Trigger Level",tooltip ="Channel,Voltage level"),pg.Button("Voltage Offset",tooltip = "Channel,V Offset"),pg.Button("Refresh Image")],
    [pg.Button("Quit")],
    
]
#our layout for the entire window
layout =[
    
    
    [pg.Column(function_column)],
    [pg.Image(key = "Image"),pg.Column(measurement_table_column)]
    ] 

   
window = pg.Window("Siglent Scope",layout)


#this constantly checks for events 
while True:
    event,values = window.read()
    
    print(values)
    
    
    
    if event =="Quit" or event == pg.WIN_CLOSED:
        break

    if event == "Go":
        command()

    if event == 'Clear':
        window["SCPI Command"].update('')

    if event =="Web Page":
        web_browser()

    if event == "Screen Dump":
        screen_dump() 

    if event == "Trigger Mode":
        trigger_mode(values[1])
        update_image()

    if event =="Voltage Division":
        volt_division(values[0],values["VDIV"]) 
        update_image() 

    if event == "Time Division":
        time_division(values["TDIV"])  
        update_image() 

    if event == "Trigger Level":
        trigger_level(values[0],values["VDIV"])
        update_image()

    if event == "Voltage Offset":
        channel_offset(values[0],values["VDIV"])
        update_image()
    if event == "Refresh Image":
        update_image()

    
        



      

end_session()
window.close() 



    
    
    
    


        
        
        
        
        
        
        
        
        