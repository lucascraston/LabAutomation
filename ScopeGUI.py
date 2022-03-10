import PySimpleGUI as pg

layout =[
    #[pg.Menu("menu 1")],
    [
    pg.Button("C1",tooltip="Channel 1",size=(10,3),button_color="White",mouseover_colors="Yellow"),
    pg.Button("C2",tooltip="Channel 2",size=(10,3),button_color="White",mouseover_colors="Red"),
    pg.Button("C3",tooltip="Channel 3",size=(10,3),button_color="White",mouseover_colors="Blue"),
    pg.Button("C4",tooltip="Channel 4",size=(10,3),button_color="White",mouseover_colors="Lime Green")],
    [pg.Button("Quit")]
    ]
window = pg.Window("Siglent Scope",layout,margins=(200,100))

def channel_one_event(message):
    print(message)

while True:
    event,values = window.read()
    print(values)
    if event =="Quit" or event == pg.WIN_CLOSED:
        break
    elif event == "C1":
        channel_one_event("C1 pressed")




window.close()    