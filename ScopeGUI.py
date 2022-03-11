
import PySimpleGUI as pg
import control_rev0 as scp
from PIL import Image
import io
import time

pg.theme("Darkteal9")

def update_image():
    time.sleep(0.75)
    file_name = scp.screen_dump()
    image = Image.open(file_name)
    bio= io.BytesIO()
    image.save(bio,format = "PNG")
    window["Image"].update(data=bio.getvalue())

layout =[
    #[pg.Menu("menu 1")],
    #pg.Button("C2",tooltip="Channel 2",size=(10,3),button_color="White",mouseover_colors="Red"),
    #pg.Button("C3",tooltip="Channel 3",size=(10,3),button_color="White",mouseover_colors="Blue"),
    #pg.Button("C4",tooltip="Channel 4",size=(10,3),button_color="White",mouseover_colors="Lime Green")],
    
    [pg.Text("Input Voltage Values(V):"),pg.InputText(key="VDIV")],
    [pg.Text("Input Time Values(S):"),pg.InputText(key="TDIV")],
    [pg.Text("Select your channel:"),pg.Combo(["C1","C2","C3","C4"]),pg.Text("Select the trigger mode:"),pg.Combo(["AUTO","NORM","SINGLE","STOP"])],
    [pg.Button("Voltage Division"),
    pg.Button("Time Division"),pg.Button("Web Page"),pg.Button("Screen Dump"),pg.Button("Trigger Mode")],
    [pg.Button("Trigger Level"),pg.Button("Voltage Offset"),pg.Button("Refresh Image")],
    [pg.Button("Quit")],
    [pg.Image(key = "Image")]
    ] 

   
window = pg.Window("Siglent Scope",layout)

while True:
    event,values = window.read()
    
    
    if event =="Quit" or event == pg.WIN_CLOSED:
        break

    if event =="Web Page":
        scp.web_browser()

    if event == "Screen Dump":
        scp.screen_dump() 

    if event == "Trigger Mode":
        scp.trigger_mode(values[1])
        update_image()

    if event =="Voltage Division":
        scp.volt_division(values[0],values["VDIV"]) 
        update_image() 

    if event == "Time Division":
        scp.time_division(values["TDIV"])  
        update_image() 

    if event == "Trigger Level":
        scp.trigger_level(values[0],values["VDIV"])
        update_image()

    if event == "Voltage Offset":
        scp.channel_offset(values[0],values["VDIV"])
        update_image()
    if event == "Refresh Image":
        update_image()    
      



window.close()    