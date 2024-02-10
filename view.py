import tkinter as tk

from components import ChatBox, TextInput, IconBtn


class ChatView(tk.Tk):
    colorscheme = {
        "primary": "#252331",
        "secondary": "#343145",
        "tertiary": "#211f2c",
        "accent": "#096ad9",
    }

    def __init__(self, title: str):
        clr = self.color

        super().__init__()

        self.wm_title(title)
        self.wm_geometry("400x500+30+30")
        self.config(bg=clr("secondary"), padx=5, pady=5)

        self.root = tk.LabelFrame(self, bg=clr("primary"), padx=2, pady=2)
        self.root.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.chatbox = ChatBox(self.root)
        self.chatbox.grid(row=0, column=0, sticky="nsew")

        self.inputbox = tk.Frame(self.root, bg=clr("primary"))
        self.inputbox.grid(row=1, column=0, sticky="sew", padx=2, pady=2)

        self.inputmsg = TextInput(self.inputbox, max_height=6)
        self.inputmsg.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.sendbtn = IconBtn(self.inputbox, "./resource/send-icon.png")
        self.sendbtn.grid(row=0, column=1, sticky="n", padx=4, pady=4)

        self.sendbtn.config(command=self.send_message)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, minsize=self.inputbox.winfo_height())
        self.root.grid_columnconfigure(0, weight=1)

        self.inputbox.grid_rowconfigure(0, weight=1)
        self.inputbox.grid_columnconfigure(0, weight=1)
        self.inputbox.grid_columnconfigure(1, minsize=40)

    def color(self, kind: str) -> str:
        return self.colorscheme[kind]

    def send_message(self):
        msg = self.inputmsg.get("1.0", "end").strip()
        if msg:
            self.chatbox.add_message("Sparrow", msg)
            self.inputmsg.delete("1.0", "end")
            self.inputmsg.configure_height()

    def mainloop(self):
        self.inputmsg.focus()
        super().mainloop()


if __name__ == "__main__":
    view = ChatView("SparrowChat")
    view.mainloop()
