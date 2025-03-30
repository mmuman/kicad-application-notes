
import json
import tempfile
import time
import os
import subprocess
import wx
import wx.html2

from kipy import KiCad
from kipy.errors import ConnectionError

from skip import Schematic

from ui.app_notes_ui import AppNotesDialog

#selected_note = None

class AppNotes(AppNotesDialog):
    def __init__(self):
        super(AppNotes, self).__init__(None)
        self.SetIcon(wx.Icon("icon.png"))
        self.kicad = KiCad()

        self.browser = wx.html2.WebView.New(parent=self.m_scrolledWindow2)
        # remove placeholder spacer
        self.webViewSizer.Remove(0)
        self.webViewSizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.browser.SetMaxSize( wx.Size( -1,-1 ) )
        self.Layout()
        self.m_scrolledWindow2.Layout()
        self.Refresh()
        self.Update()

        self.prog = wx.ProgressDialog(
            "Processing",
            "Starting...",
            100,
            self,
            wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME,
        )
        wx.Yield()
        treeRoot = self.notesTree.AddRoot("Notes by reference")

        d1 = os.getcwd() + "/notes"
        for entry in os.scandir(d1):
            if entry.is_dir():
                self.prog.Pulse(f"Scanning {entry.name}...")
                chipItem = self.notesTree.AppendItem(treeRoot, entry.name)
                wx.Yield()
                for leaf in os.scandir(entry.path):
                    print(leaf.path)
                    if leaf.is_file() and leaf.name[-5:] == '.html':
                        print(leaf.name)
                        noteName = leaf.name[0:-5].replace(f"{entry.name}_","")
                        noteItem = self.notesTree.AppendItem(chipItem, noteName, data=leaf.path)
                wx.Yield()
        self.notesTree.Expand(treeRoot)
        # avoid main window being put under KiCad
        #time.sleep(0.1)
        self.prog.Destroy()
        wx.Yield()

    def selectItem(self, event):
        #if (event.GetEventType() != event.EVT_TREE_ITEM_ACTIVATED):
        #    return
        path = self.notesTree.GetItemData(event.GetItem())
        print(path)
        selected_note = path
        if (path):
            print(path)
            with tempfile.NamedTemporaryFile(suffix=".svg") as f:
                #f.write(html.encode())
                #f.flush()
                print(f.name)
                if subprocess.run(["kicad-cli", "sch", "export", "svg", "-n", "-e", "-o", os.path.dirname(path), path.replace('.html', '.kicad_sch')]).returncode == 0:
                    print("SVG")


                #with open(path.replace('.html', '.kicad_sch'), 'r') as html:
                with open(path, 'r') as html:
                    #self.m_htmlWin2.LoadPage(path)
                    self.browser.SetPage(html=html.read(), baseUrl=f"file://{path}")

    def run(self, event):
        print(event)
        selected = self.notesTree.GetItemData(self.notesTree.GetSelection())
        if selected:
            success, form = self.browser.RunScript('Object.fromEntries((new FormData(document.getElementById("parameters"))).entries());')
            form = json.loads(form)
            print(form)
            sch = Schematic(selected.replace('.html', '.kicad_sch'))
            for ref in form:
                print(ref)
                if ref in sch.symbol:
                    print(ref)
                    #print(sch.symbol[ref])
                    print(sch.symbol[ref].property.Value.value)
                    sch.symbol[ref].property.Value.value = form[ref]
                    print(sch.symbol[ref].property.Value.value)
            # we have to make a file just for that
            with tempfile.NamedTemporaryFile(suffix=".kicad_sch") as f:
                sch.write(f.name)
                text = f.readlines()
                # skip header and UUID
                text[0] = text[0][text[0].index(b'(lib_symbols'):]
                text = b''.join(text)
                if wx.TheClipboard.Open():
                    wx.TheClipboard.SetData(wx.TextDataObject(text))
                    wx.TheClipboard.Close()
                    wx.MessageBox("Schematics copied to clipboard.", parent=self)
                    #self.EndModal(wx.ID_OK)



    def on_close(self, event):
        self.EndModal(wx.ID_OK)

if __name__ == "__main__":
    app = wx.App()
    dialog = AppNotes()
    dialog.ShowModal()
    dialog.Destroy()
