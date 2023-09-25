from nicegui import ui

import os
import json
import zipfile

import shortcuts

def find_name(title,values):
	for value in list(values):
		if title == value.replace(' ',''):
			return value

	return title

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

	Elements = {}

	data = update_data()

	def pointer(keys,start):
		if len(keys) == 1:
			return start

		return pointer(keys[1:],start[keys[0]])

	def delete_confirm(event):
		for file in Elements:
			if event.sender in Elements[file].values():
				break
		else:
			return

		dialog.open()

		Elements["DeleteFile"] = file		

	def delete_file(event):
		file = Elements["DeleteFile"]

		os.remove(os.path.join("data",file))

		Search.tables[file].set_visibility(False)
		
		dialog.close()

		ui.notify("{} Deleted".format(file))

	def update_expansion(event):
		for file in Elements:
			if event.sender in Elements[file].values():
				break
		else:
			return

		editing = Elements[file]["Edit"].visible

		if editing:
			Elements[file]["Edit"].set_visibility(False)
			Elements[file]["Save"].set_visibility(True)

			for key in Elements[file]["Key"]:
				Elements[file]["Value"][key].set_visibility(False)
				Elements[file]["Input"][key].set_visibility(True)
		else:
			Elements[file]["Edit"].set_visibility(True)
			Elements[file]["Save"].set_visibility(False)

			for key in Elements[file]["Key"]:
				Elements[file]["Value"][key].text = Elements[file]["Input"][key].value

				Elements[file]["Value"][key].set_visibility(True)
				Elements[file]["Input"][key].set_visibility(False)

				branches = key.split(".")

				target = pointer(branches,data[file])

				target[find_name(branches[-1],target)] = Elements[file]["Input"][key].value

			with open(os.path.join("data",file), "w") as file_data:
				json.dump(data[file],file_data,indent=4) 

		ui.notify(file)

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

	shortcuts.return_home()

	ui.button('Download',icon='file_download',on_click=download_files).classes('self-end')

	Search.element = ui.input('Search',on_change=update_search)

	with ui.dialog() as dialog, ui.card():
		ui.label('Are you sure?')
		
		with ui.row():
			ui.button("Cancel",icon='cancel',color='gray',on_click=dialog.close)
			ui.button("Delete",icon='delete',color='red',on_click=delete_file)

	for file in data:
		Elements[file] = {}

		with ui.expansion(file, icon='description').classes('w-full') as expansion:
			Search.tables[file] = expansion

			with ui.card():
				with ui.grid(columns=2):

					Elements[file]["Edit"] = ui.button('Edit',icon='edit',on_click=update_expansion)
					Elements[file]["Save"] = ui.button('Save',icon='save',on_click=update_expansion)
					Elements[file]["Delete"] = ui.button('Delete',icon='delete',color='red',on_click=delete_confirm)

					Elements[file]["Save"].set_visibility(False)

					Elements[file]["Key"] = {}
					Elements[file]["Value"] = {}
					Elements[file]["Input"] = {}

					for key,value in unpacker(data[file]):
						Elements[file]["Key"][key] = ui.label(key).classes('font-semibold')
						Elements[file]["Value"][key] = ui.label(value)
						Elements[file]["Input"][key] = ui.input("",value=value)

						Elements[file]["Input"][key].set_visibility(False)