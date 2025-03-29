zip: kicad-app-notes.zip

wxforms: plugins/ui/app_notes_ui.py

plugins/ui/app_notes_ui.py: plugins/ui/app_notes_ui.fbp
	wxformbuilder -g -l Python $<

kicad-app-notes.zip: wxforms
	zip -r9 $@ *.json plugins/*.* plugins/ui/*.* plugins/notes/*.*
