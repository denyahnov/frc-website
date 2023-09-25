from nicegui import ui
import img
def return_home():
	ui.button("Return Home", color='orange', icon="keyboard_return", on_click=lambda: ui.open("/"))

def content():
	ui.button("Scouting App", color='orange', icon="devices", on_click=lambda: ui.open("/scouter"))
	ui.button("Pit Scouting", color='orange', icon="devices", on_click=lambda: ui.open("/pit_scout"))
	ui.button("Leaderboard", color='orange', icon="trending_up", on_click=lambda: ui.open("/leaderboard"))
	ui.button("Livestream", color='orange', icon="live_tv", on_click=lambda: ui.open("/livestream"))
	ui.button("Scouting Data", color='orange', icon="assessment", on_click=lambda: ui.open("/data"))
