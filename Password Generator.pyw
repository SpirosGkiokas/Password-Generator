from tkinter import *
import os
import random
import ctypes as ct
from datetime import datetime 

#start size
start_width = 500
start_height = 450
#icon path
icon_path = os.path.join(os.getcwd(), "Assets", "icon.png")
#desktop and password path
desktop_path = os.path.expanduser("~/Desktop")
#letters list in str
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#@&%$?+-_'
#color vars
background_color = "#1f1f1f"
foreground_color = "#d9d9d9"

# taskbar icon
myappid = 'Password Generator' 
ct.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
################################### FUNCTIONS ###################################

# dark title bar function
def dark_title_bar():
    if os.name == 'nt':
        app.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(app.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                             ct.sizeof(value))

#################################### CLASSES ####################################
class main():
    def __init__(self, app, frame):
        #self staff again!!
        self.app = app
        self.frame = frame
        #sizes for storing differences in screen size
        self.size_15 = 0
        self.size_20= 0
        self.size_23 = 0
        #giving the values width - height
        self.current_width = IntVar()
        self.current_height = IntVar()
        #config pady frame
        self.frame.config(pady = 50)
        #call create widgets
        self.create_widgets()
        #resize event
        self.app.bind("<Configure>", self.resize)

    def create_widgets(self):
        self.give_length_label = Label(self.frame, text="Give Length Of Password:\n(8-30 Characters)")
        self.give_length_label.config(font=("Arial", 20, "bold"), background=background_color, foreground=foreground_color)
        self.give_length_label.grid(row=0, column=0, pady=20)
        self.entry = Entry(self.frame, font=("Arial", 23), justify="center")
        self.entry.grid(row=1, column=0)
        self.generate_button = Button(self.frame, text="Generate Password", command=self.check_if_num)
        self.generate_button.config(font=("Arial", 20, "bold"), border=3, cursor="hand2")
        self.generate_button.grid(row=2, column=0, pady=20)
        self.password_label = Label(self.frame, text="")
        self.password_label.config(font=("Arial", 15, "bold"), background=background_color, foreground=foreground_color)
        self.password_label.grid(row=3, column=0)
        self.button_frame = Frame(self.frame, background=background_color)
        self.button_frame.grid(row=4, column=0, pady=20)
        self.retry_button = Button(self.button_frame, text="Retry", command=self.generate_pos)
        self.retry_button.config(font=("Arial", 20, "bold"), border=3, cursor="hand2", state="disabled")
        self.retry_button.pack(side="left", padx=20)
        self.copy_button = Button(self.button_frame, text="Copy", command=self.copy)
        self.copy_button.config(font=("Arial", 20, "bold"), border=3, cursor="hand2", state="disabled")
        self.copy_button.pack(side="left", padx=20)
        self.save_button = Button(self.button_frame, text="Save", command=self.save_password)
        self.save_button.config(font=("Arial", 20, "bold"), border=3, cursor="hand2", state="disabled")
        self.save_button.pack(side="right", padx=20)

    def check_if_num(self):
        self.pass_length = self.entry.get()
        self.pass_length = self.pass_length.strip()
        try:
            self.pass_length = int(self.pass_length)
            if self.pass_length < 8 or self.pass_length > 30:
                self.entry.delete(0, END)
                self.entry.insert(0, "Invalid Input Try Again!")
            else:
                self.entry.delete(0, END)
                self.generate_pos()
        except ValueError as val:
            print(val)
            self.entry.delete(0, END)
            self.entry.insert(0, "Invalid Input Try Again!")
        
    def generate_pos(self):
        self.letter_pos = []
        print(len(letters))
        temp_num = - 1
        for count in range(0, self.pass_length):
            num = random.randint(0, len(letters) - 1)
            while num == temp_num:
                num = random.randint(0, len(letters) - 1)
            self.letter_pos.append(num)
            temp_num = num
        self.create_password()

    def create_password(self):
        password_letters = []
        for count,pos in enumerate(self.letter_pos):
            password_letters.append(letters[pos])
        self.password = "".join(password_letters)
        self.password_label['text'] = self.password
        self.retry_button.config(state="normal")
        self.save_button.config(state="normal")
        self.copy_button.config(state="normal")

    def save_password(self): 
        current_time = datetime.now()
        current_time = current_time.strftime("%m-%d-%H-%M-%S")
        name = f"{current_time}-password"
        path = f"{name}.txt"
        with open(os.path.join(desktop_path, path), "a")as create:
            create.writelines(self.password)
        self.password_label['text'] = f"File in desktop, filename: {name}\nApp Closing in 7 seconds"
        self.generate_button.config(state="disabled")
        self.retry_button.config(state="disabled")
        self.save_button.config(state="disabled")   
        self.copy_button.config(state="disabled") 
        self.app.after(7000, self.app.destroy)

    def copy(self):
        command = 'echo | set /p nul=' + self.password + '| clip'
        os.system(command)

    #resize function
    def resize(self, event):
        self.app.config(width=event.width, height=event.height)
        self.current_width.set(str(self.app.winfo_width()))
        self.current_height.set(str(self.app.winfo_height()))
        self.resize_widgets()

    #resize widgets with new vals
    def resize_widgets(self):
        percentage = ((self.current_width.get() / start_width + self.current_height.get() / start_height) / 2)
        size_15 = int(15 * percentage)
        size_20 = int(20 * percentage)
        size_23 = int(23 * percentage)
        if(size_15 != self.size_15):
            self.password_label.config(font=("Arial", size_15, "bold"))
            self.size_15 = size_15
        if(size_20 != self.size_20):
            self.give_length_label.config(font=("Arial", size_20, "bold"))
            self.give_length_label.grid_configure(pady=size_20)
            self.generate_button.config(font=("Arial", size_20, "bold"))
            self.generate_button.grid_configure(pady=size_20)
            self.button_frame.grid_configure(pady=size_20)
            self.retry_button.config(font=("Arial", size_20, "bold"))
            self.retry_button.pack_configure(padx=size_20)
            self.save_button.config(font=("Arial", size_20, "bold"))
            self.save_button.pack_configure(padx=size_20)
            self.copy_button.config(font=("Arial", size_20, "bold"))
            self.copy_button.pack_configure(padx=size_20)
            self.size_20 = size_20
        if(size_23 != self.size_23):
            self.entry.config(font=("Arial", size_23))
            self.size_23 = size_23


###################################### APP ######################################
#app instance
app = Tk()
#app config
app.title("Password Generator")
app.geometry("500x450")
app.minsize(width=500, height=450)
app.maxsize(width=1000, height=900)
app.iconphoto(False, PhotoImage(file=icon_path))
app.config(background=background_color)
dark_title_bar()

#main frame
frame = Frame(app, background=background_color)
frame.grid_columnconfigure(0, weight=1)
frame.pack(expand=True, fill='both')

#call main
main(app, frame)

#display app
app.mainloop()