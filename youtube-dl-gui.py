#!/usr/bin/python3
from __future__ import unicode_literals

import pygame
from pygame.locals import *
from pygame.scrap import *

from pgu import gui
from misClases import *

import youtube_dl

import update as u
import os

def changeStatus (new):
    '''Show/hide download end'''
    main.remove(status)
    status.value = new
    main.add(status, 770,400)

def pasteURL():
    '''Paste URL from clipboard to url input'''
    changeStatus('')
    url = pygame.scrap.get("STRING")
    if url:
        inputURL.value = url.decode("ascii", "ignore")

def inputNewName():
    '''Clear name input if it value is the default name'''
    changeStatus('')
    if inputName.value == defaultName:
        inputName.value = ''

def leaveInputName():
    '''If the user didn't write nothing, change name input value to default'''
    if inputName.value == '':
        inputName.value = defaultName

def openFileBrowser():
    '''Open dialog to select folder'''
    changeStatus('')
    d = FolderDialog(path = inputDir.value)
    d.connect(gui.CHANGE, fileBrowserClosed, d)
    d.open()

def fileBrowserClosed(dlg):
    '''When user close folder dialog, directory input value change to selection'''
    if dlg.value: inputDir.value = dlg.value

def saveDefaultDirectory():
    '''Save in a file the directory selected as default directory to download'''
    dirFile = open("directorio.txt", "w")
    dirFile.write(inputDir.value)
    dirFile.close()

def changeFormatSelection(swt,sel):
    '''Change audio/video selector'''
    changeStatus('')
    main.remove(sel[0])
    sel.pop(0)
    if swt.value:
        sel.append(audioSelect)
    else:
        sel.append(videoSelect)
    main.add(sel[0], 370, 265)

def download():
    '''Download video'''
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

def updateytdl():
    '''Update youtube-dl'''
    print("Actualizando")
    u.update()
    print("Listo")


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
    defaultDir = os.getcwd()
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

# Actualizar youtube-dl
bu = UpdateButton()
main.add(bu, 100, 400)
bu.connect(gui.CLICK, updateytdl)

# Descargar
bd = DownloadButton()
bd.connect(gui.CLICK, download)
main.add(bd, 790, 280)

# Iniciar scrap para obtener informacion del portapapeles
pygame.scrap.init()
pygame.scrap.set_mode(SCRAP_CLIPBOARD)
main.add(status, 770,400)
app.run(main)
