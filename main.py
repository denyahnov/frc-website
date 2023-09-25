from nicegui import ui

import shortcuts
import leaderboard
import livestream
import scouter
import data_page
import stats
import picklist

@ui.page('/')
def mainpage():
	ui.label("ICRobotics - Competition Homepage").classes('text-h4 font-bold text-grey-8')

	shortcuts.content()

ui.run(title="Team 5584",favicon='🤖')
