from nicegui import ui

def return_home():
	ui.button("Return Home", color='orange', icon="keyboard_return", on_click=lambda: ui.open("/"))

def content():
	tailwind = 'w-full max-w-sm'

	ui.button("Scouting App", color='orange', icon="devices", on_click=lambda: ui.open("/scouter")).classes(tailwind)
	ui.button("Leaderboard", color='orange', icon="trending_up", on_click=lambda: ui.open("/leaderboard")).classes(tailwind)
	ui.button("Livestream", color='orange', icon="live_tv", on_click=lambda: ui.open("/livestream")).classes(tailwind)
	ui.button("Team Statistics", color='orange', icon="assessment", on_click=lambda: ui.open("/stats")).classes(tailwind)
	ui.button("Picklist", icon="list", color='orange', on_click=lambda: ui.open("/picklist")).classes(tailwind)
	ui.button("Raw Scouting Data", color='orange', icon="folder", on_click=lambda: ui.open("/data")).classes(tailwind)
