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
	shortcuts.init_colors()

	class Search:
		element = None
		tables = {}
		text = ""

	Elements = {}

	def delete_confirm(event):
		for file in Elements:
			if event.sender == Elements[file]:
				break
		else:
			return

		dialog.open()

		Elements["DeleteFile"] = file		

	def delete_file(event):
		file = Elements["DeleteFile"]

		os.remove(os.path.join("imgs",file))

		Search.tables[file].set_visibility(False)
		
		dialog.close()

		ui.notify("{} Deleted".format(file))

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

	ui.button('Download',icon='file_download',on_click=download_files, color='orange').classes('self-end')

	Search.element = ui.input('Search',on_change=update_search)

	ui.label("No Photos Available").classes('text-slate-400 text-lg').set_visibility(len(data) == 0)

	with ui.dialog() as dialog, ui.card().style(f'background-color: #424242'):
		ui.label('Are you sure?').classes('font-semibold text-white')
		
		with ui.row():
			ui.button("Cancel",icon='cancel',color='gray',on_click=dialog.close)
			ui.button("Delete",icon='delete',color='red',on_click=delete_file)

	for file in data:
		with ui.expansion(file, icon='description').classes('w-full') as expansion:
			Search.tables[file] = expansion

			Elements[file] = ui.button('Delete',icon='delete',color='red',on_click=delete_confirm)

			with ui.card().style(f'background-color: #424242'):
				ui.image('/imgs/{}'.format(file)).classes("w-full max-w-sm")