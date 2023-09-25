from nicegui import ui
import shortcuts

stream_link = "https://www.youtube.com/embed/TW3HyKVL5SU?si=IcfuPAhNC6krNRGZ"

stream_embed = f'<iframe width="1020" height="630" src="{stream_link}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'

@ui.page('/livestream')
def livestream_content():
	shortcuts.init_colors()

	shortcuts.return_home()
	ui.html(stream_embed)