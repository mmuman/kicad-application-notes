
import json
import tempfile
import time
import os
import subprocess
import sys
import uuid
import wx
import wx.html2
import yaml

from jinja2 import Environment, FileSystemLoader, select_autoescape

from kipy import KiCad
from kipy.errors import ConnectionError

from skip import Schematic

from ui.app_notes_ui import AppNotesDialog

generate_all_html_on_startup = True

#selected_note = None

def generate_html(path):
    html_path = path.replace('.yml', '.html')
    if os.path.exists(html_path) and (os.path.getmtime(html_path) >= os.path.getmtime(path)):
        return True
    with open(path, 'r') as f:
        configuration = yaml.safe_load(f)
        if configuration is None:
            return False
        #print(configuration)
        env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
        template = env.get_template("note.html")
        try:
            context = {
                'basename': os.path.basename(path.replace('.yml', '')),
                'fields': {}
            }
            for k in ['title', 'script', 'intro', 'footnotes', 'references']:
                if k in configuration:
                    context[k] = configuration[k]
            params = {}
            if 'parameters' in configuration:
                params = configuration['parameters']
            for p in params:
                #print(p)
                for name in p:
                    #print(p[name])
                    field = p[name]
                    field['name'] = name
                    field['label'] = name
                    #print(field)
                    code = ""
                    extra = ""
                    if p[name]['input'] == 'text':
                        code = '<input type="text" '
                    if p[name]['input'] == 'select':
                        code = '<select '
                    code += f'id="{name}" name="{name}" '
                    code += 'onchange="updateFields();" '
                    if 'disabled' in p[name] and p[name]['disabled']:
                        code += 'disabled="disabled" '
                    if 'readonly' in p[name] and p[name]['readonly']:
                        code += 'readonly="readonly" '
                    if 'value' in p[name] and p[name]['value']:
                        code += f'value="{p[name]["value"]}" '
                    if 'SI' in p[name] and p[name]['SI']:
                        code += f'data-si="true" '
                    if p[name]['input'] == 'text':
                        if 'values' in p[name]:
                            code += f'list="{name}_values" /><datalist id="{name}_values">'
                            for v in p[name]['values']:
                                code += f'<option value="{v}">'
                            code += f'</datalist>'
                        else:
                            code += '/>'
                    if p[name]['input'] == 'select':
                        code += ' />'
                        if 'values' in p[name]:
                            for v in p[name]['values']:
                                code += f'<option name="{v}">{v}</option>'
                        code += '</select>'
                    #code += '/>'
                    if 'unit' in p[name] and p[name]['unit']:
                        code += p[name]["unit"]
                    field['code'] = code
                    context['fields'][name] = field
            #print(context)
            with open(html_path, 'w') as html:
                html.write(template.render(context))
        except Exception as e:
            print(e)
            return False
    return True



def generate_all_html():
    d1 = os.getcwd() + "/notes"
    for entry in os.scandir(d1):
        if entry.is_dir():
            print(f"Scanning {entry.name}...")
            for leaf in os.scandir(entry.path):
                print(leaf.path)
                if leaf.is_file() and leaf.name[-4:] == '.yml':
                    print(leaf.name)
                    #html_path = leaf.path.replace('.yml', '.html')
                    generate_html(leaf.path)

class AppNotes(AppNotesDialog):
    def __init__(self):
        super(AppNotes, self).__init__(None)
        self.SetIcon(wx.Icon("icon.png"))
        self.kicad = KiCad()

        self.prog = wx.ProgressDialog(
            "Processing",
            "Starting...",
            100,
            self,
            wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME,
        )
        wx.Yield()

        self.browser = wx.html2.WebView.New(parent=self.m_scrolledWindow2)
        # remove placeholder spacer
        self.webViewSizer.Remove(0)
        self.webViewSizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.browser.SetMaxSize( wx.Size( -1,-1 ) )
        self.Layout()
        self.m_scrolledWindow2.Layout()
        self.Refresh()
        self.Update()

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
                    if leaf.is_file() and leaf.name[-4:] == '.yml':
                        print(leaf.name)
                        html_path = leaf.path.replace('.yml', '.html')
                        if generate_all_html_on_startup:
                            generate_html(leaf.path)
                        noteName = leaf.name[0:-4].replace(f"{entry.name}_","")
                        noteItem = self.notesTree.AppendItem(chipItem, noteName, data=leaf.path)
                wx.Yield()
        #self.notesTree.Expand(treeRoot)
        # avoid main window being put under KiCad
        #time.sleep(0.1)
        self.prog.Destroy()
        wx.Yield()

    def selectItem(self, event):
        #if (event.GetEventType() != event.EVT_TREE_ITEM_ACTIVATED):
        #    return
        path = self.notesTree.GetItemData(event.GetItem())
        #print(path)
        selected_note = path
        if (path):
            print(path)
            html_path = path.replace('.yml', '.html') or None
            with tempfile.NamedTemporaryFile(suffix=".svg") as f:
                #f.write(html.encode())
                #f.flush()
                print(f.name)
                if subprocess.run(["kicad-cli", "sch", "export", "svg", "-n", "-e", "-o", os.path.dirname(path), path.replace('.yml', '.kicad_sch')]).returncode == 0:
                    print("SVG")

                generate_html(path)

                #with open(path.replace('.html', '.kicad_sch'), 'r') as html:
                with open(html_path, 'r') as html:
                    #self.m_htmlWin2.LoadPage(path)
                    self.browser.SetPage(html=html.read(), baseUrl=f"file://{path}")
                    #time.sleep(1)
                    #self.SetTitle("Application Notes - " + self.browser.CurrentTitle)

    def run(self, event):
        print(event)
        selected = self.notesTree.GetItemData(self.notesTree.GetSelection())
        if selected:
            success, form = self.browser.RunScript('Object.fromEntries((new FormData(document.getElementById("parameters"))).entries());')
            form = json.loads(form)
            print(form)
            # TODO: inject this and references
            note_uuid = str(uuid.uuid4())
            sch = Schematic(selected.replace('.yml', '.kicad_sch'))
            #print(sch.symbol)
            for s in sch.symbol:
                #TODO: actually clone Reference and hide it (Datasheet might not always be here?)
                # XXX: can't hide properties for now :-(
                # cf. https://github.com/psychogenic/kicad-skip/issues/8
                p = s.property.Datasheet.clone()
                p.name = 'app_note_uuid'
                p.value = note_uuid
                #p.effects.hide = True
                p = s.property.Datasheet.clone()
                p.name = 'app_note_reference'
                p.value = s.property.Reference.value
                #p.effects.hide = True
                p = s.property.Datasheet.clone()
                p.name = 'app_note_name'
                p.value = os.path.basename(selected.replace('.yml', ''))
                #p.effects.hide = True
            # TODO: replace the symbol/pin/wire UUIDs
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
    if len(sys.argv) > 1:
        generate_all_html()
        sys.exit(0)
    app = wx.App()
    dialog = AppNotes()
    dialog.ShowModal()
    dialog.Destroy()
