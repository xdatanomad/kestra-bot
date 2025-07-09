"""
Kestra Bot Demo - A Textual Terminal Application
A terminal application for building Kestra ETL Flows using OpenAI agents.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header, Footer, TabbedContent, TabPane, TextArea, Label, 
    Static, Log, Collapsible, SelectionList, Select
)
from textual.binding import Binding
from textual.reactive import reactive
from textual.message import Message
from textual import events
from typing import Any
import asyncio
import logging

from kestrabot.openai_bot import (
    get_kestrabot_client,
    KestraBotOpenAIClient,
    KestraBotFlowResponse
)
from kestrabot.settings import settings, _MODELS_


class TextualLogHandler(logging.Handler):
    """Custom logging handler that writes to a Textual Log widget."""
    
    def __init__(self, log_widget):
        super().__init__()
        self.log_widget = log_widget
    
    def emit(self, record):
        """Emit a log record to the Textual Log widget."""
        try:
            msg = self.format(record)
            # Ensure we're writing to the log widget safely
            if hasattr(self.log_widget, 'write_line') and self.log_widget.is_mounted:
                self.log_widget.write_line(msg)
        except Exception:
            # Silently ignore errors to avoid infinite recursion
            pass


class KestraBotHeader(Static):
    """Custom header widget for the Kestra Bot Demo application."""
    
    def compose(self) -> ComposeResult:
        yield Static(
            "[bold cyan]Kestra Bot Demo[/bold cyan]\n"
            "[dim]An OpenAI agent for building Kestra ETL Flows[/dim]\n"
            "[dim darkviolet]Author: Parham (parham.parvizi@gmail.com)[/dim darkviolet]",
            id="header-content"
        )


class StatusBar(Static):
    """Status bar widget to show background task status."""
    
    status_message = reactive("Ready")
    
    def compose(self) -> ComposeResult:
        yield Label(f"Status: {self.status_message}", id="status-label")
    
    def watch_status_message(self, message: str) -> None:
        """Update status message when it changes."""
        try:
            label = self.query_one("#status-label", Label)
            label.update(f"Status: {message}")
        except:
            # Label not yet mounted, ignore
            pass
    
    async def update_status(self, message: str) -> None:
        """Async method to update status message."""
        self.status_message = message


class PromptTab(TabPane):
    """Tab for user prompt input."""
    
    def __init__(self, title: str, id: str | None = None):
        super().__init__(title, id=id)
    
    def compose(self) -> ComposeResult:
        text = "Enter your prompt here. Describe what you want the Kestra Bot to do."
        # Create a TextArea for user input
        textarea = TextArea.code_editor(
            text,
            language="markdown",
            id="prompt-textarea",
            classes="tab-textarea",
            theme="dracula",
            tab_behavior="indent",
        )
        textarea.indent_type = "spaces"
        textarea.show_line_numbers = True
        yield textarea
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle prompt text area changes."""
        if event.text_area.id == "prompt-textarea":
            # Placeholder for prompt change handling
            pass


class MetadataTab(TabPane):
    """Tab for metadata input."""
    
    def __init__(self, title: str, id: str | None = None):
        super().__init__(title, id=id)
    
    def compose(self) -> ComposeResult:
        textarea = TextArea(
            language="markdown",
            id="metadata-textarea",
            classes="tab-textarea"
        )
        textarea.text = "Enter metadata information (table schema, data definitions, credentials, etc.)"
        yield textarea
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle metadata text area changes."""
        if event.text_area.id == "metadata-textarea":
            # Placeholder for metadata change handling
            pass


class KestraFlowTab(TabPane):
    """Tab for Kestra Flow YAML display/editing."""
    
    def __init__(self, title: str, id: str | None = None):
        super().__init__(title, id=id)
    
    def compose(self) -> ComposeResult:
        textarea = TextArea(
            language="yaml",
            id="flow-textarea",
            classes="tab-textarea"
        )
        textarea.text = "Generated Kestra Flow YAML will appear here..."
        yield textarea
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle flow YAML text area changes."""
        if event.text_area.id == "flow-textarea":
            # Placeholder for flow YAML change handling
            pass


class ExecutionLogsTab(TabPane):
    """Tab for execution logs and console output."""
    
    def __init__(self, title: str, id: str | None = None):
        super().__init__(title, id=id)
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            # Collapsible sections for execution history
            with Container(id="execution-history-container"):
                yield Label("Execution History", classes="section-title")
                yield VerticalScroll(id="execution-history-scroll")
                # Placeholder collapsible sections will be added dynamically
            
            # Scrollable log area
            with Container(id="console-log-container"):
                yield Label("Console Logs", classes="section-title")
                yield Log(id="console-log", classes="console-log", max_lines=200)
    
    def add_execution_log(self, execution_id: str, content: str) -> None:
        """Add a new collapsible execution log section."""
        container = self.query_one("#execution-history-scroll", VerticalScroll)
        collapsible = Collapsible(
            Label(content, classes="execution-content"),
            title=f"Execution {execution_id}",
            collapsed=True
        )
        container.mount(collapsible)
    
    def add_console_log(self, message: str) -> None:
        """Add a message to the console log."""
        log_widget = self.query_one("#console-log", Log)
        log_widget.write_line(message)


class SettingsTab(TabPane):
    """Tab for application settings."""
    
    def __init__(self, title: str, id: str | None = None):
        super().__init__(title, id=id)
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Developer Prompt", classes="section-title")
            dev_prompt_textarea = TextArea(
                language="markdown",
                id="dev-prompt-textarea",
                classes="settings-textarea"
            )
            dev_prompt_textarea.text = settings.developer_prompt or "Enter your developer prompt here. This will be used to guide generation of Kestra Flows.\n"
            yield dev_prompt_textarea
            
            yield Label("OpenAI Model Selection", classes="section-title")
            yield Select(
                [(model, model) for model in _MODELS_],
                value=settings.openai_model,
                id="model-select"
            )
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle settings text area changes."""
        if event.text_area.id == "dev-prompt-textarea":
            # Placeholder for dev prompt change handling
            pass
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle model selection changes."""
        if event.select.id == "model-select":
            # Placeholder for model selection change handling
            pass


class KestraBotApp(App):
    """Main Kestra Bot Demo application."""

    CSS = """
    /* Basic styling for the Kestra Bot Demo application */

    #header-content {
        padding: 0 0;
        text-align: center;
    }
    
    #status-label {
        height: 10%;
        padding: 0 2;
    }

    #main-tabs {
        height: 90%;
        padding: 1 2;
    }

    #execution-history-container {
        padding: 0 1;
    }

    #console-log-container {
        padding: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("1", "switch_tab('prompt')", "Prompt"),
        Binding("2", "switch_tab('metadata')", "Metadata"),
        Binding("3", "switch_tab('flow')", "Flow"),
        Binding("4", "switch_tab('logs')", "Logs"),
        Binding("5", "switch_tab('settings')", "Settings"),
        Binding("ctrl+b", "build_flow", "Build Flow"),
        Binding("ctrl+a", "add_to_kestra", "Add to Kestra"),
        Binding("ctrl+e", "execute_flow", "Execute Flow"),
    ]
    
    def __init__(self):
        super().__init__()
        self.title = "Kestra Bot Demo"
        self.sub_title = "An OpenAI agent for building Kestra ETL Flows"
    
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield KestraBotHeader()
        
        with TabbedContent(initial="prompt", id="main-tabs"):
            yield PromptTab("Prompt", id="prompt")
            yield MetadataTab("Metadata", id="metadata")
            yield KestraFlowTab("Kestra Flow", id="flow")
            yield ExecutionLogsTab("Execution Logs", id="logs")
            yield SettingsTab("Settings", id="settings")
        
        yield StatusBar()
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Set the theme
        self.theme = "tokyo-night"

        # Set up custom logging to the Log widget
        log_widget = self.query_one("#console-log", Log)
        handler = TextualLogHandler(log_widget)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))
        # Remove existing handlers to avoid duplicate logging
        root_logger = logging.getLogger()
        for existing_handler in root_logger.handlers[:]:
            root_logger.removeHandler(existing_handler)
        root_logger.addHandler(handler)
        root_logger.setLevel(settings.get_logging_level())
        logging.info("Kestra Bot Demo application started")

        # Set initial status
        status_bar = self.query_one(StatusBar)
        asyncio.create_task(status_bar.update_status("Application started"))
    
    async def action_switch_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = tab_id
        
        # Update status
        status_bar = self.query_one(StatusBar)
        await status_bar.update_status(f"Switched to {tab_id.title()} tab")
    
    async def action_build_flow(self) -> None:
        """Handle Build Flow action."""
        # Get prompt tab text area content
        prompt_textarea = self.query_one("#prompt-textarea", TextArea)
        prompt = prompt_textarea.text.strip()
        # Get Metadata tab text area content
        metadata_textarea = self.query_one("#metadata-textarea", TextArea)
        metadata = metadata_textarea.text.strip()

        # set status
        status_bar = self.query_one(StatusBar)
        await status_bar.update_status("Building Kestra Flow...")

        # Call the Kestra OpenAI client to generate the flow
        client: KestraBotOpenAIClient = get_kestrabot_client()
        try:
            response: KestraBotFlowResponse = client.generate_kestra_flow(
                user_input=prompt,
                metadata=metadata
            )
            if response.output:
                flow_textarea = self.query_one("#flow-textarea", TextArea)
                flow_textarea.text = response.output
                await status_bar.update_status("Flow generated successfully")
            else:
                raise ValueError("No output generated from the flow")
        except Exception as e:
            await status_bar.update_status(f"Error: {str(e)}")
            logs_tab = self.query_one("#logs", ExecutionLogsTab)
            logs_tab.add_console_log(f"Error generating flow: {str(e)}")
            return
        
        # Add console log
        logs_tab = self.query_one("#logs", ExecutionLogsTab)
        logs_tab.add_console_log("Build Flow action triggered")
        
        # Simulate some work
        await status_bar.update_status("Flow build completed")
    
    async def action_add_to_kestra(self) -> None:
        """Handle Add to Kestra action."""
        # Placeholder for add to Kestra functionality
        status_bar = self.query_one(StatusBar)
        await status_bar.update_status("Adding flow to Kestra...")
        
        # Add console log
        logs_tab = self.query_one("#logs", ExecutionLogsTab)
        logs_tab.add_console_log("Add to Kestra action triggered")
        
        # Simulate some work
        await asyncio.sleep(1)
        await status_bar.update_status("Flow added to Kestra")
    
    async def action_execute_flow(self) -> None:
        """Handle Execute Flow action."""
        # Placeholder for execute flow functionality
        status_bar = self.query_one(StatusBar)
        await status_bar.update_status("Executing Kestra Flow...")
        
        # Add console log
        logs_tab = self.query_one("#logs", ExecutionLogsTab)
        logging.info("Executing Kestra Flow...")
        
        # Add execution log
        import time
        execution_id = str(int(time.time()))
        logs_tab.add_execution_log(
            execution_id,
            f"Flow executed at {time.strftime('%Y-%m-%d %H:%M:%S')}\nStatus: Success\nDuration: 2.5s"
        )
        
        # Simulate some work
        await status_bar.update_status("Flow execution completed")
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


def run_app():
    """Main entry point for the application."""
    app = KestraBotApp()
    app.run()


if __name__ == "__main__":
    run_app()
