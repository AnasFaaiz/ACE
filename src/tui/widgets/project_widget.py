import os
import concurrent.futures
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, ListView, ListItem 
from rich.text import Text 

from src.features.project_manager import load_projects
from src.features.vanguard import check_project_status

class ProjectWidget(Static):
    """A dual-pane dynamic i3-style Project Hub using real registry data"""

    def __init__(self, title: str, widget_id: str = ""):
        super().__init__(id=widget_id)
        self.window_title = title
        self.can_focus = True 
        self.registered_projects = {}

    def on_mount(self) -> None:
        self.border_title = self.window_title 
        self.reload_registry()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ListView(id="project-list", classes="project-sidebar-pane")

            with VerticalScroll(classes="project-detail-pane"):
                yield Static("Select a project from the left pane to check live telemetry...", id="project-details")

    def reload_registry(self)-> None:
        """Loads projects from your projects.json and appends them to the ListView."""
        self.registered_projects = load_projects()
        list_view = self.query_one("#project-list", ListView)
        list_view.clear()

        if not self.registered_projects:
            list_view.append(ListItem(Static("No projects registered")))
            return 
        
        for nickname in self.registered_projects.keys():
            list_view.append(ListItem(Static(f" { nickname}"), id=f"p-{nickname}"))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Triggered automatically when highlighting a project using arrow keys."""
        if not event.item or not event.item.id:
            return 

        nickname = event.item.id.replace("p-", "")
        if nickname not in self.registered_projects:
            return 

        details_pane = self.query_one("#project-details", Static)
        details_pane.update(Text(f" Running thread pooled git diagnostics for '{nickname}'...", style="italic dim yellow"))

        project_info = (nickname, self.registered_projects[nickname])

        def run_async_check():
            return check_project_status(project_info)

        def handle_result(future):
            try:
                raw_output = future.result()
                clean_output = raw_output.replace("\n   ", "\n").replace("\n  ", "\n")
                details_pane.update(Text.from_markup(f"[bold cyan]Telemetry Output:[/bold cyan]\n\n{clean_output}"))
            except Exception as e:
                details_pane.update(Text(f"Diagnostics failed: {str(e)}", style="bold red"))

        worker = self.run_worker(run_async_check, thread=True)
        self.run_worker(lambda: handle_result(worker.future))
