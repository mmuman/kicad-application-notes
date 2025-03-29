zip: kicad-app-notes.zip

wxforms: plugins/ui/app_notes_ui.py

plugins/ui/app_notes_ui.py: plugins/ui/app_notes_ui.fbp
	wxformbuilder -g -l Python $<

kicad-app-notes.zip: wxforms
	zip -r9 $@ \
		metadata.json \
		resources/*.png \
		plugins/plugin.json \
		plugins/*.py \
		plugins/*.png \
		plugins/*.txt \
		plugins/ui/*.py \
		plugins/notes/*.js \
		plugins/notes/*/*.html \
		plugins/notes/*/*.kicad_sch
		unzip -lv $@ | tail -1 | \
			awk '{print "install_size: ",$$1,"\ndownload_size: ",$$2}'
		sha256sum $@
