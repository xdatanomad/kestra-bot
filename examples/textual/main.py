from textual.app import App
from textual.widgets import Button, Input, Static

class MyApp(App):
    async def on_mount(self):
        await self.view.dock(Static("Enter your name:"), edge="top")
        self.input = Input()
        await self.view.dock(self.input, edge="top")
        self.btn = Button("Submit", name="submit")
        await self.view.dock(self.btn, edge="top")

    async def on_button_pressed(self, message):
        if message.sender.name == "submit":
            await self.view.dock(Static(f"Hello, {self.input.value}!"), edge="bottom")


if __name__ == "__main__":
    app = MyApp()
    app.run()
