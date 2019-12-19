"""Clases utilizadas exclusivamente en este proyecto."""

from pgu import gui
import os

# Botones con iconos personalizados
class PasteButton(gui.Button):
    def __init__(self, **params):
        params.setdefault('cls', 'pastebutton')
        super(PasteButton, self).__init__(value="    ", **params)

class OpenButton(gui.Button):
    def __init__(self, **params):
        params.setdefault('cls', 'openbutton')
        super(OpenButton, self).__init__(value="    ", **params)

class SaveButton(gui.Button):
    def __init__(self, **params):
        params.setdefault('cls', 'savebutton')
        super(SaveButton, self).__init__(value="    ", **params)

class HelpButton(gui.Button):
    def __init__(self, **params):
        params.setdefault('cls', 'helpbutton')
        super(HelpButton, self).__init__(value="    ", **params)

class DownloadButton(gui.Button):
    def __init__(self, **params):
        params.setdefault('cls', 'downloadbutton')
        super(DownloadButton, self).__init__(value="           ", **params)

class FolderDialog(gui.Dialog):
    def __init__(self, title_txt="Seleccione carpeta", button_txt="Abrir", cls="dialog", path=None):
        """Clase para seleccionar carpetas. Es parecida a fileDialog, 
        pero no muestra archivos. Usa sus mismos elementos, excepto 
        el input_file"""

        cls1 = "filedialog"
        if not path: self.curdir = os.getcwd()
        else: self.curdir = path
        self.dir_img = gui.basic.Image(
            gui.pguglobals.app.theme.get(cls1+".folder", "", 'image'))
        self.title = gui.basic.Label(title_txt, cls=cls+".title.label")
        self.body = gui.Container(width=700, height=300)
        
        self.body.add(gui.basic.Label("Carpeta"), 10, 10)

        self.input_dir = gui.input.Input(size=38)
        self.body.add(self.input_dir, 125, 10)
 
        self.button_ok = gui.button.Button(button_txt)
        self.body.add(self.button_ok, 640, 12)
        self.button_ok.connect(gui.const.CLICK, self._button_okay_clicked_, None)

        self.list = gui.area.List(width=690, height=235)
        self.body.add(self.list, 10, 50)
        self._list_dir_()
        self.list.connect(gui.const.CHANGE, self._item_select_changed_, None)

        self.value = None
        gui.Dialog.__init__(self, self.title, self.body)

    def _list_dir_(self):
        self.input_dir.value = self.curdir
        self.input_dir.pos = len(self.curdir)
        self.input_dir.vpos = 0
        dirs = []
        try:
            for i in os.listdir(self.curdir):
                if os.path.isdir(os.path.join(self.curdir, i)): dirs.append(i)
        except:
            pass
        dirs.sort()
        dirs = ['..'] + dirs

        for i in dirs:
            self.list.add(i,image=self.dir_img,value=i)
        self.list.set_vertical_scroll(0)


    def _item_select_changed_(self, arg):
        fname = os.path.abspath(os.path.join(self.curdir, self.list.value)) 
        if os.path.isdir(fname):
            self.curdir = fname
            self.list.clear()
            self._list_dir_()


    def _button_okay_clicked_(self, arg):
        if self.input_dir.value != self.curdir:
            if os.path.isdir(self.input_dir.value):
                self.curdir = os.path.abspath(self.input_dir.value)
                self.list.clear()
                self._list_dir_()
        else:
            self.value = self.curdir
            self.send(gui.const.CHANGE)
            self.close()

class HelpDialog(gui.Dialog):
    '''Clase para mostrar como usar el programa.'''
    def __init__(self,**params):
        title = gui.Label("Ayuda")
        
        width = 900
        height = 400
        doc = gui.Document(width=width)
        
        space = title.style.font.size(" ")
        
        doc.block(align=-1)
        doc.add(gui.Image("data/themes/default/paste_button.png"))
        for word in "  Pegar url del video a descargar".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("data/themes/default/open_button.png"))
        for word in """  Seleccionar el directorio donde se va a guardar""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("data/themes/default/save_button.png"))
        for word in """  Guardar el directorio seleccionado como predeterminado""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("data/themes/default/audio_button.png"))
        doc.space(space)
        doc.add(gui.Image("data/themes/default/video_button.png"))
        for word in """  Seleccionar formato de salida""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("data/themes/default/download_button.png"))
        for word in """  Descargar el video""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        gui.Dialog.__init__(self,title,gui.ScrollArea(doc,width,height))

