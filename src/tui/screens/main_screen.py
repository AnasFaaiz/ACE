from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Static, ListItem, ListView
from rich.text import Text
from src.tui.widgets.project_widget import ProjectWidget
from src.tui.widgets.vanguard_widget import VanguardWidget

# ==============================================================================
# 1. MODULAR LAUNCHER OVERLAY
# ==============================================================================

class LauncherMenu(Container):
    """A floating menu overlay simulating a dmenu/rofi utility."""
    def compose(self) -> ComposeResult:
        yield Static("⚡ A.C.E. Launcher", id="launcher-title")
        yield ListView(
            ListItem(Static("💬 Chat Assistant"), id="launch-chat"),
            ListItem(Static("📁 Project Manager"), id="launch-projects"),
            ListItem(Static("󰊢 Vanguard (Git Status)"), id="launch-vanguard"),
            ListItem(Static("📰 News Hub RSS Reader"), id="launch-news"),
            id="launcher-list"
        )

# ==============================================================================
# 2. THE GRID CONTAINER WIDGET
# ==============================================================================

class TileWindow(Static):
    """An i3-style widget container with title, content, and keyboard focus capability."""
    def __init__(self, title: str, content: str = "", widget_id: str = ""):
        super().__init__(id=widget_id)
        self.window_title = title
        self.content = content
        # Ensure the widget can receive keyboard focus
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Static(f"■ {self.window_title}", classes="widget-title")
        yield Static(self.content, id=f"{self.id}-body")


# ==============================================================================
# 3. PRIMARY INTERACTIVE WORKSPACE
# ==============================================================================

class MainScreen(Screen):
    """The central keyboard-driven dynamic tiling screen."""
    
    BINDINGS = [
        ("/", "toggle_launcher", "Launch Service"),
        ("escape", "close_launcher", "Close Launcher"),
        ("ctrl+h", "focus_previous", "Prev Panel"),
        ("ctrl+l", "focus_next", "Next Panel"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        # We start with a single default landing status dashboard
        yield Grid(
            TileWindow(
                "A.C.E. Dashboard", 
                "System Online. All parameters normal.\n\nPress '/' to open a workspace panel.",
                widget_id="module-dashboard"
            ),
            id="workspace"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Initially focus the main dashboard."""
        self.query_one("#module-dashboard").focus()

    def action_toggle_launcher(self) -> None:
        """Toggles the presence of the popup dmenu launcher."""
        try:
            # If launcher is already open, remove it
            launcher = self.query_one("#launcher-overlay")
            launcher.remove()
        except Exception:
            # Mount it floating at the screen root layer
            self.mount(LauncherMenu(id="launcher-overlay"))
            self.query_one("#launcher-list").focus()

    def action_close_launcher(self) -> None:
        """Closes the launcher popup safely."""
        try:
            self.query_one("#launcher-overlay").remove()
        except Exception:
            pass

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selecting an item from our launcher."""
        item_id = event.item.id
        workspace = self.query_one("#workspace", Grid)
        
        if item_id == "launch-vanguard":
            widget_id = "module-vanguard"
            try:
                workspace.query_one(f"#{widget_id}").focus()
            except Exception:
                workspace.mount(VanguardWidget("Vanguard (Git monitor)", widget_id = widget_id))
                self.call_after_refresh(workspace.query_one(f"#{widget_id}").focus)

        elif item_id == "launch-projects":
            widget_id = "module-projects"
            try:
                workspace.query_one(f"#{widget_id}").focus()
            except Exception:
                workspace.mount(ProjectWidget("Project Hub (Registry Overview)", widget_id=widget_id))
                self.call_after_refresh(workspace.query_one(f"#{widget_id}").focus)
               
        else:
            mapping = {
                "launch-chat": ("Chat Assistant", "Chat log loaded. Waiting for LLM connectivity...", "module-chat"),
                "launch-news": ("News Hub", "RSS synchronizing with HackerNews...", "module-news")
            }
            if item_id in mapping:
                title, description, widget_id = mapping[item_id]
                try:
                    workspace.query_one(f"#{widget_id}").focus()
                except Exception:
                    workspace.mount(TileWindow(title, description, widget_id=widget_id))
                    self.call_after_refresh(workspace.query_one(f"#{widget_id}").focus)

        try:
            dashboard = workspace.query_one("#module-dashboard")
            if len(workspace.children) > 1:
                dashboard.remove()
        except Exception:
            pass

        # Adjust the tiling grid dynamically based on the number of panels running
        self.recalculate_grid(workspace)
        self.action_close_launcher()

    def recalculate_grid(self, workspace: Grid) -> None:
        """Recalculates the dynamic grid dimension ratios."""
        count = len(workspace.children)
        if count <= 1:
            workspace.styles.grid_size_x = 1
            workspace.styles.grid_size_y = 1
        elif count == 2:
            workspace.styles.grid_size_x = 2
            workspace.styles.grid_size_y = 1
        else:
            workspace.styles.grid_size_x = 2
            workspace.styles.grid_size_y = (count + 1) // 2
