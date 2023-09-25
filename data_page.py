from nicegui import ui

import os
import json
import zipfile

import shortcuts

def JoinName(title,text):
	if title != "":
		return title + "." + text.replace(' ','')

	return text

def unpacker(tree,title=""):
	output = []

	for branch in tree:

		if type(tree[branch]) == dict:
			output += unpacker(tree[branch],JoinName(title,branch))

		else:
			output.append((JoinName(title,branch), tree[branch]))

	return output

def update_data():
	data = {}

	folder = "data"

	for file in os.listdir(folder):
		with open(os.path.join(folder, file), "r") as file_data:
			data[file] = json.load(file_data)

	return data

@ui.page('/data')
def data_page_content():
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

		name = "scout_data.zip"

		with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
			for file in files:
				zip_ref.write(os.path.join("data",file))

		zip_ref.close()

		ui.download(name)

	data = update_data()

	shortcuts.return_home()

	ui.button('Download',icon='file_download',on_click=download_files).classes('self-end')

	Search.element = ui.input('Search',on_change=update_search)

	for file in data:
		with ui.expansion(file, icon='description').classes('w-full') as expansion:
			Search.tables[file] = expansion

			with ui.card():
				with ui.grid(columns=2):
					for key,value in unpacker(data[file]):
						ui.label(key).classes('font-semibold')
						ui.label(value)

