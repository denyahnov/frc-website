from nicegui import ui

import os
import json

import shortcuts

from tba import *

all_teams = TBA.get_teams()

drivebases = ["Swerve", "Mecanum", "Tank", "Other"]

@ui.page('/pitscouter')
def pitscouter_content():

	class Elements:
		game_pieces = {}

	def save_data():
		title = "PIT_{}".format(Elements.team_number.value)

		data = {
			"Team": Elements.team_number.value,
			"Drivebase": Elements.drivebase.value,
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

	with ui.card():
		ui.label("Drivebase Type:").classes('font-bold')
		Elements.drivebase = ui.radio(drivebases, value=drivebases[-1]).props('inline')

	### PICKUP/INTAKE LOCATIONS ###

	with ui.row():
		with ui.card():
			ui.label("Cone Pickup:").classes('font-bold')

			Elements.cone_pickup = [
				ui.switch("Upright Ground"),
				ui.switch("Knocked Ground"),
				ui.switch("Single Substation"),
				ui.switch("Double Substation")
			]

		with ui.card():
			ui.label("Cube Pickup:").classes('font-bold')

			Elements.cube_pickup = [
				ui.switch("Ground"),
				ui.switch("Single Substation"),
				ui.switch("Double Substation")
			]

	### SCORING LOCATIONS ###

	with ui.card():
		ui.label("Scoring Locations:").classes('font-bold')

		with ui.grid(columns=2):
			for location in ["High","Mid","Low"]:
				for piece in ["Cone","Cube"]:
					title = f"{location} {piece}"

					Elements.game_pieces[title] = ui.switch(title)

	### SUBMIT DATA ###

	with ui.row():
		ui.button('Submit Data', icon='save', on_click=submit)
		Elements.spinner = ui.spinner(size='lg')

		Elements.spinner.set_visibility(False)