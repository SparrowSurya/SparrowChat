import tkinter as tk

from typing import Dict, Any


class IconBtn(tk.Button):
    style: Dict[str, Any] = {
        "background": "#252331",
        "activebackground": "#252331",
        "highlightthickness": 0,
        "justify": "center",
        "anchor": "center",
        "borderwidth": 0,
        "relief": "flat",
        "overrelief": "flat",
        "compound": "center",
    }

    def __init__(self, master: tk.Misc, icon_path: str):
        self.icon_path = icon_path
        self.image = tk.PhotoImage(file=self.icon_path)
        super().__init__(master, **self.style, image=self.image)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Demo IconBtn")
    root.config(bg="#252331")

    img_file = "./resource/demo-iconbtn.png"

    widget = IconBtn(root, img_file)
    widget.pack()

    root.mainloop()
