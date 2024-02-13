import tkinter as tk
import tkinter.font as tkfont

import sys
from functools import cached_property
from typing import Dict, Any


class MsgHead(tk.Label):
    style: Dict[str, Any] = {
        "foreground": "#ff66b7",
        "background": "#343145",
        "font": {
            "family": "Roboto",
            "size": 12,
            "weight": "bold",
            "underline": 1,
        },
        "height": 1,
        "justify": "left",
        "anchor": "nw",
    }

    def __init__(self, master: tk.Misc, text: str):
        font_dict = self.style.pop("font")
        self.style["font"] = (
            tkfont.Font(**font_dict) if isinstance(font_dict, dict) else font_dict
        )

        super().__init__(master, **self.style, text=text)


class MsgBody(tk.Label):
    style: Dict[str, Any] = {
        "foreground": "#d7d7da",
        "background": "#343145",
        "font": {
            "family": "Roboto",
            "size": 14,
            "weight": "normal",
        },
        "justify": "left",
        "anchor": "nw",
    }

    def __init__(self, master: tk.Misc, text: str):
        font_dict = self.style.pop("font")
        self.style["font"] = (
            tkfont.Font(**font_dict) if isinstance(font_dict, dict) else font_dict
        )

        super().__init__(master, **self.style, text=text)

        self.bind("<Configure>", lambda _: self.configure_wrap())

    # NOTE: assumes that text content is not changed
    @cached_property
    def text_width(self) -> int:
        return self.style["font"].measure(self.cget("text"))

    # NOTE: below method can cause infinite callbacks on window with no explicit geometry value
    # Hence do provide geometry to the window
    def configure_wrap(self):
        self.config(wraplength=self.master.winfo_width())


class Notification(tk.Label):
    style: Dict[str, Any] = {
        "foreground": "#656881",
        "background": "#343145",
        "font": {
            "family": "Roboto",
            "size": 14,
            "weight": "normal",
        },
        "justify": "center",
        "anchor": "center",
    }

    def __init__(self, master: tk.Misc, text: str):
        font_dict = self.style.pop("font")
        self.style["font"] = (
            tkfont.Font(**font_dict) if isinstance(font_dict, dict) else font_dict
        )

        super().__init__(master, **self.style, text=text)


class MsgBox(tk.Frame):
    style: Dict[str, Any] = {
        "background": "#343145",
        "padx": 2,
        "pady": 2,
    }

    def __init__(self, master: tk.Misc):
        super().__init__(master, **self.style)


class ChatBox(tk.Frame):
    style: Dict[str, Any] = {
        "background": "#252331",
        "padx": 2,
        "pady": 2,
    }

    def __init__(self, master: tk.Misc):
        super().__init__(master, **self.style)

        self._canvas = tk.Canvas(
            self,
            background=self.style["background"],
            highlightthickness=0,
            borderwidth=0,
        )
        self._canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.frame = tk.Frame(self._canvas, **self.style, bg=self.style["background"])
        self.frame_id = self._canvas.create_window(
            0, 0, anchor=tk.NW, window=self.frame
        )

        self.frame.bind("<Configure>", lambda _: self.configure_frame())
        self._canvas.bind("<Configure>", lambda _: self.configure_canvas())

        if sys.platform == "win32":
            self._canvas.bind("<MouseWheel>", self._on_scroll)
            self.bind_class("scroll-chat", "<MouseWheel>", self._on_scroll)
        elif sys.platform == "linux":
            self._canvas.bind("<Button-4>", self._on_scroll)
            self._canvas.bind("<Button-5>", self._on_scroll)
            self.bind_class("scroll-chat", "<Button-4>", self._on_scroll)  # scroll-up
            self.bind_class("scroll-chat", "<Button-5>", self._on_scroll)  # scroll-down
        else:
            print("Chat Scroll is not supported for you system")

        self.listen_scroll(self.frame)

    def configure_frame(self):
        w, h = self.frame.winfo_reqwidth(), self.frame.winfo_reqheight()
        self._canvas.config(scrollregion=(0, 0, w, h))
        self._canvas.config(width=w)

    def configure_canvas(self):
        self._canvas.itemconfigure(self.frame_id, width=self._canvas.winfo_width())

    if sys.platform == "win32":

        def _on_scroll(self, e: tk.Event):
            self._canvas.yview_scroll(-(e.delta // 120), "units")

    elif sys.platform == "linux":

        def _on_scroll(self, e: tk.Event):
            if e.num == 4:
                self._canvas.yview_scroll(-1, "units")
            elif e.num == 5:
                self._canvas.yview_scroll(1, "units")

    else:

        def _on_scroll(self, e: tk.Event):
            pass

    def add_message(self, head: str, body: str):
        box = MsgBox(self.frame)
        box.pack(fill=tk.X, padx=2, pady=5)

        title = MsgHead(box, head)
        title.pack(fill=tk.X, anchor=tk.NW)

        content = MsgBody(box, body)
        content.pack(fill=tk.X, anchor=tk.SW)

        self.listen_scroll(box, title, content)

        # NOTE: below call might result in infinite loop of callbacks
        # see MsgBody.configure_wrap
        self.frame.update_idletasks()
        self._canvas.yview_moveto(1)

    def add_notification(self, msg: str):
        box = MsgBox(self.frame)
        box.pack(fill=tk.X, padx=2, pady=5)

        notifi = Notification(box, msg)
        notifi.pack(expand=tk.TRUE, padx=10, pady=3, anchor=tk.CENTER)

        self.listen_scroll(box, notifi)

        # NOTE: below call might result in infinite loop of callbacks
        # see MsgBody.configure_wrap
        self.frame.update_idletasks()
        self._canvas.yview_moveto(1)

    def listen_scroll(self, *widgets: tk.Widget):
        for widget in widgets:
            widget.bindtags(("scroll-chat",) + widget.bindtags())


msgs = (
    ("Shelly", "Hey there, ready for another round? Let's show 'em what we've got!"),
    ("Bull", "Yeehaw! I'm always up for some action. Let's charge in and dominate!"),
    ("Jessie", "I've got my turret ready to go. Who's up for some strategic mayhem?"),
    (
        "Poco",
        "♪ Let's make some music and heal up, team! Together, we're unstoppable! ♪",
    ),
    ("El Primo", "¡Hola, amigos! El Primo is here to bring the heat. Who's with me?"),
    ("Penny", "Avast, ye landlubbers! Time to set sail and plunder some treasure!"),
    (
        "Mortis",
        "Beware, mortals! The night beckons. Who's brave enough to face the darkness?",
    ),
    (
        "Bo",
        "Stealth is key. Let's set up some traps and catch 'em off guard, shall we?",
    ),
    (
        "Nita",
        "Let's unleash the power of the bear and roar to victory! Are you with me?",
    ),
)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x400+30+30")
    root.config(bg="#252331", padx=6, pady=6)

    chat = ChatBox(root)
    chat.pack(fill=tk.BOTH, padx=3, pady=3, expand=tk.TRUE)

    for user, msg in msgs:
        print(user)
        chat.add_message(user, msg)
        if user == "Poco":
            chat.add_notification("Nita joined the chat")

    root.mainloop()
