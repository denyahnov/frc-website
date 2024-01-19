import img
import shortcuts
import os
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

from tba import *

all_teams = TBA.get_teams()
all_rounds = TBA.get_schedule()

driver_stations = ['Blue 1', 'Blue 2', 'Blue 3', 'Red 1', 'Red 2', 'Red 3']

cycle_time_rating = ["N/A","Slow (25+ secs)", "Medium (25-15 secs)", "Fast (15> secs)"]

climb_rating = ["Did not Attempt", "Parked", "Climbed"]

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

		auto_scoring = [0] * 5
		teleop_scoring = [0] * 5

	class Variables:
		sending_data = False

	class Elements:
		auto_scoring = []
		teleop_scoring = []

	def find_counter(event, is_auto = False, increment = 1, limit = 9):
		if is_auto:
			element_list = Elements.auto_scoring
			variable_list = Data.auto_scoring
		else:
			element_list = Elements.teleop_scoring
			variable_list = Data.teleop_scoring

		target_id = event.sender.id - increment

		for i,element in enumerate(element_list):
			if element.id == target_id:

				if variable_list[i] == limit:
					return

				variable_list[i] += increment

				element.set_text(variable_list[i])

	def auto_score(event: ValueChangeEventArguments):
		find_counter(event, True, 1, 99)

	def auto_unscore(event: ValueChangeEventArguments):
		find_counter(event, True, -1, 0)

	def teleop_score(event: ValueChangeEventArguments):
		find_counter(event, False, 1, 99)

	def teleop_unscore(event: ValueChangeEventArguments):
		find_counter(event, False, -1, 0)

	def Counter(text, is_teleop = True):
		ui.label("%s:" % text)

		with ui.row():
			ui.button("-",color='red-600', on_click=teleop_unscore if is_teleop else auto_unscore).classes('text-slate-100')

			if is_teleop:
				Elements.teleop_scoring.append(ui.label("0").classes("text-amber-400 text-2xl font-bold"))
			else:
				Elements.auto_scoring.append(ui.label("0").classes("text-amber-400 text-2xl font-bold"))

			ui.button("+",color='green-600', on_click=teleop_score if is_teleop else auto_score).classes('text-slate-100')

	driver_stations = ['Blue 1', 'Blue 2', 'Blue 3', 'Red 1', 'Red 2', 'Red 3']

	def save_data():
		title = "{}_{}_{}".format(Elements.match_type.value[0],Data.round_number,Data.team_number)

		data = {
			"Match": Elements.match_type.value,
			"Round": Data.round_number,
			"Station": driver_stations[Data.driver_station],
			"Team": int(Data.team_number),
			"Autonomous":{
				"Has Autonomous": int(Elements.has_autonomous.value),
				"Crossed Autonomous Line": int(Elements.crossed_line.value),
				"Alliance Notes": int(Elements.alliance_notes.value),
				"Centerline Notes": int(Elements.centerline_notes.value),
				"Scoring": {
					"Rings Scored": int(Data.auto_scoring[0]),
					"Rings Missed": int(Data.auto_scoring[1]),
					"Amp Scored": int(Data.auto_scoring[2]),
					"Trap Scored": int(Data.auto_scoring[3]),
				},
			},
			"Teleoperated":{
				"Scoring": {
					"Rings Scored": int(Data.teleop_scoring[0]),
					"Rings Missed": int(Data.teleop_scoring[1]),
					"Amp Scored": int(Data.teleop_scoring[2]),
					"Trap Scored": int(Data.teleop_scoring[3]),
				},
				"Endgame": {
					"Trap Scored": int(Data.teleop_scoring[4]),
					"Climb": int(climb_rating.index(Elements.climb.value)),
					"Microphones": int(Elements.microphones.value),
				},
				"Extra":{
					"Coop Pressed": int(Elements.coop_pressed.value),
					"Subsystem Failure": int(Elements.subsystem_failure.value),
					"Complete Robot Failure": int(Elements.robot_failure.value),
				},
			},
			"Comments": {
				"Cycle Speed": int(cycle_time_rating.index(Elements.rate_cycle.value)),
				"Driving": int(str(Elements.rate_driving.value).replace("N/A","0")),
				"Defence": int(str(Elements.rate_defence.value).replace("N/A","0")),
				"Notes": Elements.notes.value,
			},
		}

		with open(os.path.join("data","{}.json".format(title)), "w") as file:
			json.dump(data,file,indent=4)

		ui.notify(title)

	def submit():
		Elements.spinner.set_visibility(True)

		save_data()

		ui.notify("Saved Successfully!")

		Elements.spinner.set_visibility(False)

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
	Elements.crossed_line = ui.switch('Crossed Autonomous Line')

	ui.label("Alliance Notes Collected")
	Elements.alliance_notes = ui.toggle([0,1,2,3], value=0)
	
	ui.label("Centerline Notes Collected")
	Elements.centerline_notes = ui.toggle([0,1,2,3,4,5], value=0)

	Elements.auto_rings_scored = Counter("Speakers Scored", False)
	Elements.auto_rings_missed = Counter("Speakers Missed", False)
	Elements.auto_amp_scored = Counter("Amps Scored", False)
	Elements.auto_trap_scored = Counter("Traps Scored", False)

	### TELEOPERATED ###
	Header("Teleoperated")

	Elements.coop_pressed = ui.switch('Co-op Bonus Pressed')
	Elements.subsystem_failure = ui.switch('Subsystem Failure')
	Elements.robot_failure = ui.switch('Complete Robot Failure')

	Elements.teleop_rings_scored = Counter("Speakers Scored", True)
	Elements.teleop_rings_missed = Counter("Speakers Missed", True)
	Elements.teleop_amp_scored = Counter("Amps Scored", True)
	Elements.teleop_trap_scored = Counter("Traps Scored Before Endgame", True)

	Header("Endgame")
	
	ui.label("Stage")
	Elements.climb = ui.toggle(climb_rating, value=climb_rating[0])

	Elements.teleop_trap_scored = Counter("Traps Scored During Endgame", True)

	ui.label("Microphones Scored")
	Elements.microphones = ui.toggle([0,1,2,3], value=0)


	### RATINGS ###
	Header("Comments")

	with ui.card():

		ui.label('Cycle Speed:')
		Elements.rate_cycle = ui.toggle(cycle_time_rating, value="N/A")

		ui.label('Driving Rating:')
		Elements.rate_driving = ui.toggle(["N/A",1,2,3,4,5], value="N/A")

		ui.label('Defence Rating:')
		Elements.rate_defence = ui.toggle(["N/A",1,2,3,4,5], value="N/A")

	### NOTES ###

	with ui.card():
		Elements.notes = ui.textarea(label='Notes', placeholder='Type here...',)

	### SUBMIT DATA ###

	with ui.row():
		ui.button('Submit Data', icon='save', on_click=submit)
		Elements.spinner = ui.spinner(size='lg')

		Elements.spinner.set_visibility(False)