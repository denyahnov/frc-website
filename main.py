from nicegui import ui

import shortcuts
import leaderboard
import livestream
import scouter
import data_page
import stats
import picklist
import pit_scouter
import img


@ui.page('/')
def mainpage():
	ui.image(img.IC).classes("h-20 w-20"), ui.label("ICRobotics - Competition Homepage").classes('text-h4 font-bold text-white')
	ui.query('body').style(f'background-color: #424242')
	shortcuts.content()

ui.run(title="Team 5584",favicon='🤖')
