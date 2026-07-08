import os
import asyncio
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, ListView, ListItem
from rich.text import Text

# Import native vanguard and project manager logic
from src.features.vanguard import run_command, check_project_status
from src.features.project_manager import load_projects

class VanguardWidget(Static):
    """A keyboard-focused operational command grid for automated Git security tracking."""

    def __init__(self, title: str, widget_id: str = ""):
        super().__init__(id=widget_id)
        self.window_title = title
        self.can_focus = True
        self.projects_cache = {}

    def on_mount(self) -> None:
        self.border_title = self.window_title
        self.refresh_vanguard_targets()

    def compose(self) -> ComposeResult:
        with Horizontal():
            # Left Control Panel: Target Project Selection
            yield ListView(id="vanguard-target-list", classes="vanguard-sidebar")
            
            # Right Panel: Real-time Repository Diagnostics & Branch Safety Warnings
            with VerticalScroll(classes="vanguard-console"):
                yield Static("Select an active repository to run safety audits...", id="vanguard-log")

    def refresh_vanguard_targets(self) -> None:
        """Populates the tracking sidebar with registered workspaces."""
        self.projects_cache = load_projects()
        list_view = self.query_one("#vanguard-target-list", ListView)
        list_view.clear()

        if not self.projects_cache:
            list_view.append(ListItem(Static("🔒 No targets configured")))
            return

        for name in self.projects_cache.keys():
            list_view.append(ListItem(Static(f"🛡️  {name}"), id=f"v-{name}"))
    
    BINDINGS = [
        ("r", "refresh_audit", "Refresh Status"),
        ("a", "stage_all", "Stage All Changes (git add .)")
    ]

    def action_refresh_audit(self) -> None:
        """Manually force-trigger the audit on the highlighted item."""
        list_view = self.query_one("#vanguard-target-list", ListView)
        if list_view.highlighted_child:
        # Re-trigger the highlighted event logic
            list_view.post_message(ListView.Highlighted(list_view, list_view.highlighted_child))

    async def action_stage_all(self) -> None:
        """Runs a quick staging macro for the selected repository."""
        list_view = self.query_one("#vanguard-target-list", ListView)
        if not list_view.highlighted_child or not list_view.highlighted_child.id:
            return
        
        nickname = list_view.highlighted_child.id.replace("v-", "")
        project_path = self.projects_cache[nickname]['local_path']
    
        await asyncio.to_thread(run_command, "git add .", cwd=project_path)
        self.action_refresh_audit()

    async def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Triggered automatically via arrow keys to audit repositories safely."""
        if not event.item or not event.item.id:
            return

        nickname = event.item.id.replace("v-", "")
        if nickname not in self.projects_cache:
            return

        project_path = self.projects_cache[nickname]['local_path']
        log_pane = self.query_one("#vanguard-log", Static)
        log_pane.update(Text(f"🛡️ Auditing branch topology for '{nickname}'...", style="italic dim cyan"))

        def run_safety_audit():
            # 1. Branch verification
            branch, b_err = run_command("git rev-parse --abbrev-ref HEAD", cwd=project_path)
            if b_err:
                return f"[bold red]Execution Aborted:[/bold red] Not inside a functional Git tracking tree."
            
            # 2. Detailed tracking status
            status_output, _ = run_command("git status -s", cwd=project_path)
            formatted_status = []

            if status_output:
                for line in status_output.splitlines():
                    if line.startswith("M"):
                        formatted_status.append(f"[yellow]⚡ {line}[/yellow]")  # Modified
                    elif line.startswith("D"):
                        formatted_status.append(f"[red]❌ {line}[/red]")       # Deleted
                    elif line.startswith("??"):
                        formatted_status.append(f"[cyan]❓ {line}[/cyan]")     # Untracked
                    elif line.startswith("A"):
                        formatted_status.append(f"[green]➕ {line}[/green]")   # Added
                    else:
                        formatted_status.append(line)
                status_summary = "\n".join(formatted_status)
            else:
                status_summary = "[dim green]✔ No uncommitted modifications detected. Tree clean.[/dim green]"
            
            # 3. Format telemetry payload
            is_protected = branch in ["main", "master", "prod"]
            security_shield = "[bold red]🛑 PROD BRANCH LOCKOUT ENGAGED[/bold red]" if is_protected else "[bold green]✅ STAGING SAFE[/bold green]"
            
            report = (
                f"[bold cyan]Repository Registry Key:[/bold cyan] {nickname}\n"
                f"[bold cyan]Target Mount Path:[/bold cyan] {project_path}\n"
                f"[bold cyan]Active Branch Topology:[/bold cyan] [yellow]'{branch}'[/yellow] ({security_shield})\n"
                f"────────────────────────────────────────────────────────────\n"
                f"[bold magenta]Current Staging Vector Delta (git status):[/bold magenta]\n\n{status_output}"
            )
            return report

        try:
            # Safely delegate the blocking git shell commands to a separate worker thread
            report_text = await asyncio.to_thread(run_safety_audit)
            log_pane.update(Text.from_markup(report_text))
        except Exception as ex:
            log_pane.update(Text(f"❌ Structural security verification failed: {str(ex)}", style="bold red"))
