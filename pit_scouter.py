from nicegui import ui

import os
import json

import shortcuts

from tba import *

if not os.path.exists("imgs"):
	os.mkdir("imgs")

all_teams = TBA.get_teams()

drivebases = ["Swerve", "Mecanum", "Tank", "Other"]

@ui.page('/pitscouter')
def pitscouter_content():
	shortcuts.init_colors()

	class Elements:
		game_pieces = {}

	def upload_photo(event):
		Elements.spinner2.set_visibility(True)

		counter = 0

		while True:
			title = "{}_{}.{}".format(Elements.team_number.value, counter, event.name.split(".")[-1])
	
			if title.split(".")[0] not in os.listdir("imgs"):
				break

			counter += 1

		with event.content as content:
			with open(os.path.join("imgs",title),"wb") as file:
				file.write(content.read())

		ui.notify("Uploaded {}!".format(title))

		Elements.spinner2.set_visibility(False)

	def save_data():
		title = "PIT_{}".format(Elements.team_number.value)

		data = {
			"Team": Elements.team_number.value,
			"Drivebase": Elements.drivebase.value,
			"Pickup": {
				"Cone": {
					element.text: int(element.value) for element in Elements.cone_pickup
				},
				"Cube": {
					element.text: int(element.value) for element in Elements.cube_pickup
				},
			},
			"Score": {
				location: int(Elements.game_pieces[location].value) for location in Elements.game_pieces
			},
			"Autonomous": {
				"Has Autonomous": int(Elements.has_autonomous.value),
				"Score Gamepiece": int(Elements.auto_score.value),
				"Balance Charge Station": int(Elements.auto_charge_station.value),
			},
			"Comments": Elements.comments.value,
		}

		with open(os.path.join("data","{}.json".format(title)), "w") as file:
			json.dump(data,file,indent=4)

		ui.notify(title)

	def submit():
		Elements.spinner.set_visibility(True)

		save_data()

		ui.notify("Saved Successfully!")

		Elements.spinner.set_visibility(False)

	shortcuts.return_home()

	### TEAM SELECT ###

	Elements.team_number = ui.select(label='Team Number', options=all_teams, with_input=True)

	### DRIVEBASE ###

	with ui.card().style("background-color: #595959"):
		ui.label("Drivebase Type:").classes('font-bold')
		Elements.drivebase = ui.radio(drivebases, value=drivebases[-1]).props('inline')

	### PICKUP/INTAKE LOCATIONS ###

	with ui.row():
		with ui.card().style("background-color: #595959"):
			ui.label("Cone Pickup:").classes('font-bold')

			Elements.cone_pickup = [
				ui.switch("Upright Ground"),
				ui.switch("Knocked Ground"),
				ui.switch("Single Substation"),
				ui.switch("Double Substation")
			]

		with ui.card().style("background-color: #595959"):
			ui.label("Cube Pickup:").classes('font-bold')

			Elements.cube_pickup = [
				ui.switch("Ground"),
				ui.switch("Single Substation"),
				ui.switch("Double Substation")
			]

	### SCORING LOCATIONS ###

	with ui.card().style("background-color: #595959"):
		ui.label("Scoring Locations:").classes('font-bold')

		with ui.grid(columns=2):
			for location in ["High","Mid","Low"]:
				for piece in ["Cone","Cube"]:
					title = f"{location} {piece}"

					Elements.game_pieces[title] = ui.switch(title)

	### AUTONOMOUS ###

	with ui.card().style("background-color: #595959"):
		ui.label("Autonomous:").classes('font-bold')

		Elements.has_autonomous = ui.switch("Has Autonoumous")
		Elements.auto_score = ui.switch("Score Gamepiece")
		Elements.auto_charge_station = ui.switch("Balance Charge Station")

	### COMMENTS ###

	with ui.card().style("background-color: #595959"):
		Elements.comments = ui.textarea(label='Notes', placeholder='Type here...',)

	### PHOTOS ###

	with ui.row():
		Elements.photo_upload = ui.upload(
			label="Upload Robot Photos", 
			on_upload=upload_photo, 
			multiple=True, 
			auto_upload=True
		).props("accept=image/*")

		Elements.spinner2 = ui.spinner(size='lg')

		Elements.spinner2.set_visibility(False)

	### SUBMIT DATA ###

	with ui.row():
		ui.button('Submit Data', icon='save', on_click=submit)
		Elements.spinner = ui.spinner(size='lg')

		Elements.spinner.set_visibility(False)