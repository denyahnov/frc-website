from nicegui import ui
import shortcuts
from tba import *

@ui.page('/leaderboard')
def leaderboard_content():
	shortcuts.init_colors()

	shortcuts.return_home()

	leaderboard = TBA.get_rankings()

	columns = [
		{'name': 'rank', 'label': 'Rank', 'field': 'rank', 'sortable': True, 'align': 'left'},
		{'name': 'team', 'label': 'Team', 'field': 'team'}
	]

	columns += [{'name': f"sort{i}", 'label': sort.name, 'field': f"sort{i}", 'sortable': True} for i,sort in enumerate(leaderboard.sort_order_info)]

	rows = [{"rank": team.rank, "team": team.team_key.strip('frc')} | {f"sort{i}": team.sort_orders[i] for i in range(len(team.sort_orders))} for team in leaderboard.rankings]

	ui.table(columns=columns, rows=rows, row_key='rank').classes('text-white no-shadow border-[3px]').style(f'background-color: #424242')