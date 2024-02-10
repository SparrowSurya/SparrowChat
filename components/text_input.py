import tkinter as tk
import tkinter.font as tkfont

from typing import Dict, Any


class TextInput(tk.Text):
    style: Dict[str, Any] = {
        "foreground": "#b8b8b8",
        "background": "#252331",
        "selectforeground": "#252331",
        "selectbackground": "#b8b8b8",
        "highlightbackground": "#b8b8b8",
        "highlightcolor": "#184ef6",
        "highlightthickness": 1,
        "insertbackground": "#b8b8b8",
        "insertwidth": 2,
        "insertborderwidth": 0,
        "font": {
            "family": "Roboto",
            "size": 16,
            "weight": "normal",
        },
        "wrap": "word",
        "tabs": 4,
        "height": 1,
    }

    def __init__(self, master: tk.Misc, max_height: int = 6):
        self.max_height = max_height

        font_dict = self.style.pop("font")
        self.style["font"] = font = (
            tkfont.Font(**font_dict) if isinstance(font_dict, dict) else font_dict
        )

        tabsize = self.style.pop("tabs")
        self.style["tabs"] = font.measure(" " * tabsize * 2)

        super().__init__(master, self.style)

        self.bind("<MouseWheel>", self._on_scroll)

        events = ("<<Undo>>", "<<Redo>>", "<<Cut>>", "<<Paste>>", "<KeyRelease>")
        for event in events:
            self.bind(event, lambda _: self.configure_height(), "+")

    def configure_height(self):
        height = int(self.index("end - 1c").split(".")[0])
        self.config(height=min(height, self.max_height))

    def _on_scroll(self, e: tk.Event):
        self.yview_scroll(-(e.delta // 120), "units")


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Demo TextBox")

    widget = TextInput(root, 5)
    widget.pack()

    root.mainloop()
