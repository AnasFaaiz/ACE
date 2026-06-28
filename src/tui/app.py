from textual.app import App 
from src.tui.screens.main_screen import MainScreen 

class AceTUI(App):
    """The main Textual application for ACE"""

    CSS_PATH = "styles/ace.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Force Quit")
    ]

    def on_mount(self)-> None:
        """SAet the initial screen."""
        self.push_screen(MainScreen())
