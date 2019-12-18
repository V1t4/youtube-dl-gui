import pygame
from pygame.locals import *

from pgu import gui
from misClases import *
screen = pygame.display.set_mode((1100,480),SWSURFACE)
pygame.display.set_caption("youtube-dl")

app = gui.Desktop()
app.connect(gui.QUIT, app.quit, None)
main = gui.Container(width=1100, height=500)

def btn_clk (arg):
    print("Clicked!")

def open_file_browser(arg):
    d = FolderDialog()
    d.connect(gui.CHANGE, handle_file_browser_closed, d)
    d.open()

def handle_file_browser_closed(dlg):
    if dlg.value: inputDir.value = dlg.value

def input_cb():
    print("Input received")

def swt_clk(swt,sel):
    print("Switched: ",swt.value)
    main.remove(sel[0])
    sel.pop(0)
    if swt.value:
        sel.append(audioSelect)
    else:
        sel.append(videoSelect)
    main.add(sel[0], 370, 265)

# URL
main.add(gui.Label("URL:"), 20, 30)
inputURL = gui.Input(size=70)
inputURL.connect("activate", input_cb)
main.add(inputURL, 95, 30)
bp = PasteButton()
main.add(bp, 1030, 20)
bp.connect(gui.CLICK, btn_clk, None)

# Nombre
main.add(gui.Label("Nombre:"), 20, 110)
inputName = gui.Input(value="(Nombre del video)", size=70)
inputName.connect("activate", input_cb)
main.add(inputName, 140, 110)

# Directorio
main.add(gui.Label("Directorio:"), 20, 190)
# leer input de un archivo y sobreescribirlo
inputDir = gui.Input("(Lugar donde se va a guardar)",59)
main.add(inputDir, 160, 190)
bo = OpenButton()
main.add(bo, 955, 180)
bo.connect(gui.CLICK, open_file_browser, None)
bs = SaveButton()
main.add(bs, 1030, 180)
bs.connect(gui.CLICK, btn_clk, None)

# Formato
audioSelect = gui.Select(value="mp3")
audioSelect.add("mp3","mp3")
audioSelect.add("wav","wav")
audioSelect.add("m4a","m4a")
videoSelect = gui.Select(value="mp4")
videoSelect.add("mp4","mp4")
videoSelect.add("mkv","mkv")
videoSelect.add("webm","webm")
videoSelect.add("flv","flv")
sel = []
sel.append(audioSelect)

auvi = gui.Switch()
main.add(auvi, 20, 260)
auvi.connect(gui.CLICK, swt_clk, auvi, sel)
main.add(gui.Label("Formato:"), 250,270)
main.add(sel[0], 370, 265)

# Ayuda
bh = HelpButton()
bh.connect(gui.CLICK, btn_clk, None)
main.add(bh, 20, 400)

# Descargar
bd = DownloadButton()
bd.connect(gui.CLICK, btn_clk, None)
main.add(bd, 800, 280)
app.run(main)
