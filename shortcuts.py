from nicegui import ui

def init_colors():
	ui.query('body').style(f'background-color: #424242')
	ui.colors(primary='orange', secondary='#424242', accent='#595959')

def return_home():
	ui.button("Return Home", color='orange', icon="keyboard_return", on_click=lambda: ui.open("/"))

def content():
	tailwind = 'w-full max-w-sm'

	ui.button("Scouting App", color='orange', icon="devices", on_click=lambda: ui.open("/scouter")).classes(tailwind)
	ui.button("Pit Scouter", color='orange', icon="search", on_click=lambda: ui.open("/pitscouter")).classes(tailwind)
	ui.button("Schedule", color='orange', icon="calendar_month", on_click=lambda: ui.open("/schedule")).classes(tailwind)
	ui.button("Leaderboard", color='orange', icon="trending_up", on_click=lambda: ui.open("/leaderboard")).classes(tailwind)
	ui.button("Team Statistics", color='orange', icon="assessment", on_click=lambda: ui.open("/stats")).classes(tailwind)
	ui.button("Picklist", color='orange', icon="list", on_click=lambda: ui.open("/picklist")).classes(tailwind)
	ui.button("Livestream", color='orange', icon="live_tv", on_click=lambda: ui.open("/livestream")).classes(tailwind)
	ui.button("Robot Photos", color='orange', icon="collections", on_click=lambda: ui.open("/photos")).classes(tailwind)
	ui.button("Raw Scouting Data", color='orange', icon="folder", on_click=lambda: ui.open("/data")).classes(tailwind)