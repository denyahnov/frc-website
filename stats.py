from nicegui import ui
import shortcuts

from tba import *

@ui.page('/stats')
def stats_page_content():
	shortcuts.init_colors()
	
	shortcuts.return_home()

