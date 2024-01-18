import img
import shortcuts
import os
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

from tba import *

all_teams = TBA.get_teams()
all_rounds = TBA.get_schedule()

driver_stations = ['Blue 1', 'Blue 2', 'Blue 3', 'Red 1', 'Red 2', 'Red 3']

def Header(text):
	ui.separator()
	return ui.label(text).classes('text-h4 font-bold text-grey-8')

@ui.page('/scouter')
def scouter_content():
	shortcuts.init_colors()
	
	class Data:
		round_number = 0
		driver_station = 0
		team_number = 0

		auto_game_pieces = [[0 for x in range(3)] for y in range(2)]
		teleop_game_pieces = [[0 for x in range(3)] for y in range(2)]

	class Variables:
		sending_data = False

	class Elements:
		auto_game_pieces = [[None for x in range(3)] for y in range(2)]
		teleop_game_pieces = [[None for x in range(3)] for y in range(2)]

	driver_stations = ['Blue 1', 'Blue 2', 'Blue 3', 'Red 1', 'Red 2', 'Red 3']

	def save_data():
		title = "{}_{}_{}".format(Elements.match_type.value[0],Data.round_number,Data.team_number)

		data = {
			"Match": Elements.match_type.value,
			"Round": Data.round_number,
			"Station": driver_stations[Data.driver_station],
			"Team": int(Data.team_number),
			"Score":{
				"Autonomous":{
					"Has Autonomous": int(Elements.has_autonomous.value),
					"Left Community": int(Elements.left_community.value),
					"Crossed Autonomous Line": int(Elements.crossed_line.value),
					"Charge Station": Elements.auto_charge_station.value,
				},
				"Teleoperated":{
					"Subsystem Failure": int(Elements.subsystem_failure.value),
					"Complete Robot Failure": int(Elements.robot_failure.value),
					"Charge Station": Elements.teleop_charge_station.value,
				},
			},
			"Comments": {

				"Driving": int(str(Elements.rate_driving.value).replace("N/A","0")),
				"Defence": int(str(Elements.rate_defence.value).replace("N/A","0")),
				"Durability": int(str(Elements.rate_durability.value).replace("N/A","0")),
				"Notes": Elements.notes.value,
			},
		}

		for p,piece in enumerate(["Cone","Cube"]):
			for pos,position in enumerate(["High","Mid","Low"]):
				data["Score"]["Autonomous"]["{} {}s".format(position,piece)] = Data.auto_game_pieces[p][pos]

		for p,piece in enumerate(["Cone","Cube"]):
			for pos,position in enumerate(["High","Mid","Low"]):
				data["Score"]["Teleoperated"]["{} {}s".format(position,piece)] = Data.teleop_game_pieces[p][pos]

		with open(os.path.join("data","{}.json".format(title)), "w") as file:
			json.dump(data,file,indent=4)

		ui.notify(title)

	def submit():
		Elements.spinner.set_visibility(True)

		save_data()

		ui.notify("Saved Successfully!")

		Elements.spinner.set_visibility(False)

	def find_counter(event, is_auto = False, increment = 1, limit = 9):
		if is_auto:
			elemlist = Elements.auto_game_pieces
			varlist = Data.auto_game_pieces
		else:
			elemlist = Elements.teleop_game_pieces
			varlist = Data.teleop_game_pieces

		target_id = event.sender.id - increment

		for p,piece in enumerate(elemlist):
			for e,element in enumerate(piece):
				if element.id == target_id:

					if varlist[p][e] == limit:
						return

					varlist[p][e] += increment

					element.set_text(varlist[p][e])

	def auto_score_gamepiece(event: ValueChangeEventArguments):
		find_counter(event, True, 1, 9)

	def auto_unscore_gamepiece(event: ValueChangeEventArguments):
		find_counter(event, True, -1, 0)

	def teleop_score_gamepiece(event: ValueChangeEventArguments):
		find_counter(event, False, 1, 9)

	def teleop_unscore_gamepiece(event: ValueChangeEventArguments):
		find_counter(event, False, -1, 0)

	def update_team(event: ValueChangeEventArguments):
		if event.sender.id == Elements.round_number.id:
			try:
				Data.round_number = int(event.value)
			except ValueError:
				pass

		if event.sender.id == Elements.driver_station.id:
			Data.driver_station = driver_stations.index(event.value)

		if str(Data.round_number) in all_rounds:
			Data.team_number = all_rounds[str(Data.round_number)][Data.driver_station]

		Elements.team_number.set_value(Data.team_number)

	shortcuts.return_home()

	### MATCH & TEAM SELECT ###
	Header("Team Select")

	Elements.match_type = ui.radio(['Practice', 'Qualifier'], value='Practice', on_change=update_team).props('inline')

	with ui.row():
		Elements.round_number = ui.input('Round', on_change=update_team)
		Elements.driver_station = ui.select(driver_stations, value=driver_stations[0], on_change=update_team)

	with ui.row():
		Elements.team_number = ui.select(label='Team Number', options=all_teams, with_input=True)

	### AUTONOMOUS ###
	Header("Autonomous")

	Elements.has_autonomous = ui.switch('Has Autonoumous')
	Elements.left_community = ui.switch('Left Community')
	Elements.crossed_line = ui.switch('Crossed Autonomous Line')

	ui.label('Charge Station Outcome:')

	Elements.auto_charge_station = ui.toggle(["Did not Attempt", "Failed", "Docked", "Charged"], value="Did not Attempt")

	with ui.card():
		with ui.row():
			ui.image(img.cone).classes("h-12 w-12")
			ui.image(img.cube).classes("h-12 w-12")
			
		for i in range(3):
			with ui.row():
				ui.button("-",color='red-600', on_click=auto_unscore_gamepiece).classes('text-slate-100')
				Elements.auto_game_pieces[0][i] = ui.label("0").classes("text-amber-400 text-2xl font-bold")
				ui.button("+",color='green-600', on_click=auto_score_gamepiece).classes('text-slate-100')

				ui.button("-",color='red-600', on_click=auto_unscore_gamepiece).classes('text-slate-100')
				Elements.auto_game_pieces[1][i] = ui.label("0").classes("text-violet-600 text-2xl font-bold")
				ui.button("+",color='green-600', on_click=auto_score_gamepiece).classes('text-slate-100')

	### TELEOPERATED ###
	Header("Teleoperated")

	Elements.subsystem_failure = ui.switch('Subsystem Failure')
	Elements.robot_failure = ui.switch('Complete Robot Failure')

	ui.label('Charge Station Outcome:')

	Elements.teleop_charge_station = ui.toggle(["Did not Attempt", "Failed", "Docked", "Charged"], value="Did not Attempt")

	with ui.card():
		with ui.row():
			ui.image(img.cone).classes("h-12 w-12")
			ui.image(img.cube).classes("h-12 w-12")
			
		for i in range(3):
			with ui.row():
				ui.button("-",color='red-600', on_click=teleop_unscore_gamepiece).classes('text-slate-100')
				Elements.teleop_game_pieces[0][i] = ui.label("0").classes("text-amber-400 text-2xl font-bold")
				ui.button("+",color='green-600', on_click=teleop_score_gamepiece).classes('text-slate-100')

				ui.button("-",color='red-600', on_click=teleop_unscore_gamepiece).classes('text-slate-100')
				Elements.teleop_game_pieces[1][i] = ui.label("0").classes("text-violet-600 text-2xl font-bold")
				ui.button("+",color='green-600', on_click=teleop_score_gamepiece).classes('text-slate-100')

	### RATINGS ###
	Header("Comments")

	with ui.card():

		ui.label('Driving Rating:')
		Elements.rate_driving = ui.toggle(["N/A",1,2,3,4,5], value="N/A")

		ui.label('Defence Rating:')
		Elements.rate_defence = ui.toggle(["N/A",1,2,3,4,5], value="N/A")

		ui.label('Durability Rating:')
		Elements.rate_durability = ui.toggle(["N/A",1,2,3,4,5], value="N/A")

	### NOTES ###

	with ui.card():
		Elements.notes = ui.textarea(label='Notes', placeholder='Type here...',)

	### SUBMIT DATA ###

	with ui.row():
		ui.button('Submit Data', icon='save', on_click=submit)
		Elements.spinner = ui.spinner(size='lg')

		Elements.spinner.set_visibility(False)