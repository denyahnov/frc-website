from nicegui import ui
import shortcuts

from tba import *

columnDefs = [
	{'headerName': 'Rank', 'field': 'rank', 'width': 50},
	{'headerName': 'Team', 'field': 'team', 'width': 300, 'rowDrag': True},
]

rowData = [{'rank': team.rank, 'team': team.team_key.strip('frc')} for i,team in enumerate(TBA.get_rankings().rankings)]

@ui.page('/picklist')
def picklist_content():
	shortcuts.return_home()

	ui.aggrid({
		'defaultColDef': {
			'resizable': True,
		},
		'columnDefs': columnDefs,
		'rowData': rowData,
		'rowDragManaged': True,
	})\
	.classes('h-screen w-full')