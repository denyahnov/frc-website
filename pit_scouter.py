from nicegui import ui

import os
import json

import shortcuts

from tba import *

if not os.path.exists("imgs"):
	os.mkdir("imgs")

all_teams = TBA.get_teams()

drivebases = ["Swerve", "Mecanum", "Tank", "Other"]
climb_time = ["N/A", "15+ secs", "15-10 secs", "10-5 secs", "5> secs"]

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
				"Ground": int(Elements.ground_pickup.value),
				"Source": int(Elements.source_pickup.value),
			},
			"Score": {
				"Speaker": int(Elements.score_speaker.value),
				"Amp": int(Elements.score_amp.value),
				"Trap": int(Elements.score_trap.value),
			},
			"Endgame": {
				"Climb": int(Elements.climb.value),
				"Climb Speed": int(climb_time.index(Elements.climb_time.value)),
			},
			"Autonomous": {
				"Has Autonomous": int(Elements.has_autonomous.value),
				"Score Gamepiece": int(Elements.auto_score.value),
				"Alliance Notes": int(Elements.alliance_notes.value),
				"Centerline Notes": int(Elements.centerline_notes.value),
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

	with ui.card().style("background-color: #595959"):
		ui.label("Note Pickup:").classes('font-bold')
		
		Elements.ground_pickup = ui.switch("Ground")
		Elements.source_pickup = ui.switch("Source")

	### SCORING LOCATIONS ###

	with ui.card().style("background-color: #595959"):
		ui.label("Scoring Locations:").classes('font-bold')
		
		Elements.score_speaker = ui.switch("Speaker")
		Elements.score_amp = ui.switch("Amp")
		Elements.score_trap = ui.switch("Trap")

	### ENDGAME ###
	with ui.card().style("background-color: #595959"):
		ui.label("Endgame:").classes('font-bold')
		Elements.climb = ui.switch("Can Climb")
		Elements.climb_time = ui.toggle(climb_time, value=climb_time[0])

	### AUTONOMOUS ###

	with ui.card().style("background-color: #595959"):
		ui.label("Autonomous:").classes('font-bold')

		Elements.has_autonomous = ui.switch("Has Autonomous")
		Elements.auto_score = ui.switch("Score Gamepiece")
		Elements.alliance_notes = ui.switch("Collect Alliance Notes")
		Elements.centerline_notes = ui.switch("Collect Centerline Notes")

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