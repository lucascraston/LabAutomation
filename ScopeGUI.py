import PySimpleGUI as pg
import control_rev0 as scp
pg.theme("Darkteal9")

layout =[
    #[pg.Menu("menu 1")],
    #pg.Button("C2",tooltip="Channel 2",size=(10,3),button_color="White",mouseover_colors="Red"),
    #pg.Button("C3",tooltip="Channel 3",size=(10,3),button_color="White",mouseover_colors="Blue"),
    #pg.Button("C4",tooltip="Channel 4",size=(10,3),button_color="White",mouseover_colors="Lime Green")],
    
    [pg.Text("Input Voltage Division(V):"),pg.InputText(key="VDIV")],
    [pg.Text("Input Time Division(S):"),pg.InputText(key="TDIV")],
    [pg.Text("Select your channel:"),pg.Combo(["C1","C2","C3","C4"]),pg.Text("Select the trigger mode:"),pg.Combo(["NORM","AUTO","SINGLE"])],
    [pg.Button("Voltage Division"),
    pg.Button("Time Division"),pg.Button("Web Page"),pg.Button("Screen Dump"),pg.Button("Trigger Mode")],
    [pg.Button("Quit")]
    ]
window = pg.Window("Siglent Scope",layout)

def channel_one_event(message):
    print(message)



while True:
    event,values = window.read()
    print(event,values)
    
    if event =="Quit" or event == pg.WIN_CLOSED:
        break
    if event =="Web Page":
        scp.web_browser()
    if event == "Screen Dump":
        scp.screen_dump() 
    if event == "C1":
        channel_one_event("C1 pressed")
    if event == "Trigger Mode":
        scp.trigger_mode(values[1])

    if event =="Voltage Division":
        scp.volt_division(values[0],values["VDIV"])  
    if event == "Time Division":
        scp.time_division(values["TDIV"])    


window.close()    