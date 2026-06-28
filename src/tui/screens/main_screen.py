from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, RichLog, Static
from rich.text import Text 

class Sidebar(Static):
    """Left Sidebar for future ACE navigations"""
    def comppose(self) -> ComposeResult:
        yield Static("ACE MModule\n\n> Chat\n- Projects\n- Vanguard\n- NewsHub")

class MainScreen(Screen):
    """The primary chat and command interface"""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Sidebar(id="sidebar")

        #Main Content 
        with Vertical(id="main-area"):
            yield RichLog(id="chat-log", wrap=True, highlight=True)
            yield Input(placeholder="Send a command to ACE...", id="chat-input")

        yield Footer()
    
    def on_mount(self)-> None:
        """Called when the screen is mounted."""
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(Text.from_markup("[bold cyan]System:[/bold cyan] ACE Environment Initialized. Ready for input."))
        self.query_one("#chat-input").focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle the user ressing Enter in the input"""
        user_text = event.value.strip()
        if not user_text:
            return

        chat_log = self.query_one("#chat-log", RichLog)

        chat_log.write(Text.from_markup(f"[bold green]You:[/bold green] {user_text}"))

        chat_log.write(Text.from_markup(f"[bold magenta]ACE:[/bold magenta] Echo received: '{user_text}'"))

        event.input.value = ""

