from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Vertical
# from textual.events import ButtonPressed

class MyApp(App):
    CSS_PATH = None  # Optional: define a CSS file if needed

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Enter your name:"),
            Input(id="name_input"),
            Button("Submit", id="submit_btn"),
        )

    async def on_button_pressed(self, event) -> None:
        if event.button.id == "submit_btn":
            input_widget = self.query_one("#name_input", Input)
            await self.mount(Static(f"Hello, {input_widget.value}!"), after=event.button)

if __name__ == "__main__":
    app = MyApp()
    app.run()
