#!/usr/bin/python3
from __future__ import unicode_literals

import pygame
from pygame.locals import *
from pygame.scrap import *

from pgu import gui
from misClases import *

import youtube_dl

def changeStatus (new):
    main.remove(status)
    status.value = new
    main.add(status, 770,400)

def pasteURL():
    changeStatus('') 
    url = pygame.scrap.get("STRING")
    if url:
        inputURL.value = url.decode("ascii", "ignore")

def inputNewName():
    changeStatus('') 
    if inputName.value == defaultName:
        inputName.value = ''

def leaveInputName():
    if inputName.value == '':
        inputName.value = defaultName

def openFileBrowser():
    changeStatus('') 
    d = FolderDialog(path = inputDir.value)
    d.connect(gui.CHANGE, fileBrowserClosed, d)
    d.open()

def fileBrowserClosed(dlg):
    if dlg.value: inputDir.value = dlg.value

def saveDefaultDirectory():
    dirFile = open("directorio.txt", "w")
    dirFile.write(inputDir.value)
    dirFile.close()

def changeFormatSelection(swt,sel):
    changeStatus('') 
    main.remove(sel[0])
    sel.pop(0)
    if swt.value:
        sel.append(audioSelect)
    else:
        sel.append(videoSelect)
    main.add(sel[0], 370, 265)

def download():
    url = inputURL.value
    if url == '':
        return
    name = inputName.value
    directory = inputDir.value
    form = sel[0].value
    isVideo = auvi.value
    ydl_opts = {}

    if isVideo:
        if form == "mkv":
            ydl_opts["merge_output_format"] = form
        else:
            ydl_opts["format"] = form
    else:
        ydl_opts["postprocessors"] = [{"key": "FFmpegExtractAudio",
            "preferredcodec": form}]
    fullpath = directory + '/' 
    if name == defaultName:
        fullpath += "%(title)s.%(ext)s"
    else:
        fullpath += name + ".%(ext)s"
    ydl_opts["outtmpl"] = fullpath
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    changeStatus("Finalizado exitosamente") 

screen = pygame.display.set_mode((1100,500),SWSURFACE)
pygame.display.set_caption("youtube-dl")

app = gui.Desktop()
app.connect(gui.QUIT, app.quit, None)
main = gui.Container(width=1100, height=500)

status = gui.Label("")

# URL
main.add(gui.Label("URL:"), 20, 30)
inputURL = gui.Input(size=70)
main.add(inputURL, 95, 30)
bp = PasteButton()
main.add(bp, 1030, 20)
bp.connect(gui.CLICK, pasteURL)

# Nombre
main.add(gui.Label("Nombre:"), 20, 110)
defaultName = "(Ingrese el nombre del video)"
inputName = gui.Input(value=defaultName, size=70)
inputName.connect(gui.FOCUS, inputNewName)
inputName.connect(gui.BLUR, leaveInputName)
main.add(inputName, 140, 110)

# Directorio
main.add(gui.Label("Directorio:"), 20, 190)
try:
    dirFile = open("directorio.txt")
    defaultDir = dirFile.readline()
    dirFile.close()
except FileNotFoundError:
    defaultDir = "/home/vita/Programacion"
inputDir = gui.Input(defaultDir, 59)
main.add(inputDir, 160, 190)
bo = OpenButton()
main.add(bo, 955, 180)
bo.connect(gui.CLICK, openFileBrowser)
bs = SaveButton()
main.add(bs, 1030, 180)
bs.connect(gui.CLICK, saveDefaultDirectory)

# Formato
audioSelect = gui.Select(value="mp3")
audioSelect.add("mp3","mp3")
audioSelect.add("wav","wav")
audioSelect.add("m4a","m4a")
videoSelect = gui.Select(value="mp4")
videoSelect.add("mp4","mp4")
videoSelect.add("mkv","mkv")
sel = []
sel.append(audioSelect)
audioSelect.connect(gui.CLICK,changeStatus,"")
videoSelect.connect(gui.CLICK,changeStatus,"")
auvi = gui.Switch()
main.add(auvi, 20, 260)
auvi.connect(gui.CLICK, changeFormatSelection, auvi, sel)
main.add(gui.Label("Formato:"), 250,270)
main.add(sel[0], 370, 265)

# Ayuda
bh = HelpButton()
dh = HelpDialog()
bh.connect(gui.CLICK, dh.open)
main.add(bh, 20, 400)

# Descargar
bd = DownloadButton()
bd.connect(gui.CLICK, download)
main.add(bd, 790, 280)

# Iniciar scrap para obtener informacion del portapapeles
pygame.scrap.init()
pygame.scrap.set_mode(SCRAP_CLIPBOARD)
main.add(status, 770,400)
app.run(main)
