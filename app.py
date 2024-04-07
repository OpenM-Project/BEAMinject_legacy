"""
BEAMinject GUI app

This code is experimental, check out our GitHub repository:
https://github.com/OpenM-Project/BEAMinject for more info
"""
__version__ = "0.2.0"

import sys
import threading
import customtkinter
import BEAMinjector


app = customtkinter.CTk()
app.geometry("480x300")
app.resizable(False, False)
app.title(f"BEAMinject {__version__}")
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


# Injection logic
def write_logs(widget, text):
    widget.configure(state=customtkinter.NORMAL)
    widget.insert(customtkinter.END, text)
    widget.configure(state=customtkinter.DISABLED)
    widget.see(customtkinter.END)

def start_inject():
    for widget in frame.winfo_children()[1:]:
        widget.destroy()
    logwidget = customtkinter.CTkTextbox(frame, state='disabled', width=450, height=150)
    logwidget.pack(pady=10, padx=10)
    BEAMinjector.launchmc = launchmc.get()
    BEAMinjector.write_logs = lambda x: write_logs(logwidget, x)
    BEAMinjector.quitfunc = quit_button
    thread = threading.Thread(target=BEAMinjector.main, args=())
    thread.start()

def quit_button():
    quitbtn = customtkinter.CTkButton(master=frame, command=lambda: app.destroy() == sys.exit())
    quitbtn.pack(pady=0, padx=0)
    quitbtn.configure(text="Quit")



# UI components
###############

# Frame
frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

title = customtkinter.CTkLabel(master=frame, justify=customtkinter.LEFT)
title.pack(pady=10, padx=5)
title.configure(text="BEAMinject", font=("", 30))


# Injection start
startbutton = customtkinter.CTkButton(master=frame, command=start_inject)
startbutton.pack(pady=10, padx=10)
startbutton.configure(text="Let's go!")


# Launch MC
launchmc = customtkinter.IntVar()
launchmc.set(1)
launchswitch = customtkinter.CTkSwitch(master=frame, variable=launchmc)
launchswitch.pack(pady=30, padx=10)
launchswitch.configure(text="Launch Minecraft")

# Theme Switch
currenttheme = customtkinter.IntVar()
if customtkinter.get_appearance_mode() == "Light":
    currenttheme.set(1)
def updatetheme():
    if currenttheme.get():
        customtkinter.set_appearance_mode("light")
    else:
        customtkinter.set_appearance_mode("dark")
themeswitch = customtkinter.CTkSwitch(master=frame, variable=currenttheme, command=updatetheme)
themeswitch.pack(pady=25, padx=10, side=customtkinter.LEFT)
themeswitch.configure(text="Light Mode")


# Start app
app.mainloop()
