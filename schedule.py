from nicegui import ui
import shortcuts
from tba import *

@ui.page('/schedule')
def leaderboard_content():
	shortcuts.init_colors()

	shortcuts.return_home()

	schedule = TBA.get_schedule()

	ui.label("TODO!")
	ui.label("- Match Number")
	ui.label("- Match Time")
	ui.label("- Driver Station (Bumper Color)")
	ui.label("- Alliance Partner Report -> Who can climb?")
	ui.label("- Opponent Report: -> Do you press the button? Are you going to win note race? Defence Heavy?")
