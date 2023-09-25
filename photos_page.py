from nicegui import ui, app

import os
import json
import zipfile

import shortcuts

app.add_static_files('/imgs', 'imgs')

def get_files():
	return os.listdir("imgs")

@ui.page('/photos')
def photos_page_content():
	class Search:
		element = None
		tables = {}
		text = ""

	def update_search(event):
		for title,expansion in Search.tables.items():
			if Search.element.value in title:
				expansion.set_visibility(True)
			else:
				expansion.set_visibility(False)

	def download_files(event):
		files = [title for title in Search.tables if Search.element.value in title]

		if len(files) == 0: return

		name = "robot_photos.zip"

		with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
			for file in files:
				zip_ref.write(os.path.join("imgs",file))

		zip_ref.close()

		ui.download(name)

	data = get_files()

	shortcuts.return_home()

	ui.button('Download',icon='file_download',on_click=download_files).classes('self-end')

	Search.element = ui.input('Search',on_change=update_search)

	ui.label("No Photos Available").classes('text-slate-400 text-lg').set_visibility(len(data) == 0)

	for file in data:
		with ui.expansion(file, icon='description').classes('w-full') as expansion:
			Search.tables[file] = expansion

			with ui.card():
				ui.image('/imgs/{}'.format(file)).classes("w-full max-w-sm")