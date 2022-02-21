from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
from String_Methods import *
import subprocess


class CodeEditor(Tk):
    editor_font_size = 15

    def __init__(self):
        super().__init__()
        self.FILE_PATH = ''
        self.status_bar=BooleanVar()
        self.status_bar.set(True)
        self.separator = ': ' if self.FILE_PATH != '' else ''
        self.title(f"Code Editor{self.separator}{self.FILE_PATH}")
        self.state("zoomed")
        self.iconbitmap("./code editor.ico")

        # main frame
        self.main_frame = Frame(self)
        self.main_frame.pack()

        
        # main menu
        self.main_menu = Menu(self)
        self.first_menu = Menu(self.main_menu, tearoff=0)
        self.first_menu.add_command(
            label=unifrom_separation("New File", "Ctrl+N", 15), command=self.new)
        self.first_menu.add_command(label=unifrom_separation(
            "Open File", "Ctrl+O", 15), command=self.open)
        self.recent_files = Menu(self.first_menu, tearoff=0)
        self.first_menu.add_separator()
        self.first_menu.add_command(label=unifrom_separation(
            "Save", "Ctrl+S", 15), command=self.save)
        self.first_menu.add_command(label=unifrom_separation(
            "Run", "Ctrl+R", 15), command=self.run)
        self.main_menu.add_cascade(menu=self.first_menu, label="File")
        self.run_button=Menu(self.main_menu)
        self.main_menu.add_command(label="Run",command=self.run)
        self.settings=Menu(self.main_menu,tearoff=0)
        self.settings.add_command(label="Change Font Size",command=self.change_font_size)
        self.settings.add_checkbutton(label="Show Status Bar",onvalue=1,offvalue=0,variable=self.status_bar, command=self.show_status_bar)
        self.main_menu.add_cascade(menu=self.settings,label="Settings")

        self.main_window = PanedWindow(
            self.main_frame, orient=VERTICAL, sashpad=2)
        
        # editor window
        self.editor = Text(
            self.main_window,
            width=self.winfo_screenwidth(),
            height=20,
            font=("jetbrains mono", self.editor_font_size),
        )
        self.editor.pack()

        #Key Bindings
        self.editor.bind("<Control_L><s>", lambda event: self.save())
        self.editor.bind("<Control_L><o>", lambda event: self.open())
        self.editor.bind("<Control_L><n>", lambda event: self.new())
        self.editor.bind("<Control_L><r>", lambda event: self.run())
        self.editor.bind("<Key>",lambda event:self.counter())

        self.main_window.add(self.editor)
        self.config(menu=self.main_menu)

        self.output = Text(
            self.main_window,
            width=self.winfo_screenwidth(),
            height=9,
            font=("jetbrains mono", self.editor_font_size),
            state=DISABLED,
        )
        self.output.pack()
        self.main_window.add(self.output)
        self.main_window.pack(fill=BOTH, expand=1)
        self.char_count=Label(self.main_frame,text="chars: 0",font=("Poppins SemiBold",8),width=500,anchor="w",bg="#FFFFFF")
        self.char_count.place(x=8,y=755)
        self.main_window.configure(sashrelief=RAISED)
        # adding colors to the code editor
        Percolator(self.editor).insertfilter(ColorDelegator())
        Percolator(self.output).insertfilter(ColorDelegator())


    def save(self, event=None):
        code = self.editor.get("1.0", END).rstrip()
        if self.FILE_PATH == '':
            path = asksaveasfilename(filetypes=[("Python Files", "*.py")])
            self.FILE_PATH = path
        with open(self.FILE_PATH, 'w') as f:
            f.write(code)
        self.separator = ': ' if self.FILE_PATH != '' else ''
        self.title(f"Code Editor{self.separator}{self.FILE_PATH}")
    
    def change_font_size(self):
        font_value=8
        def font_resizer(value):
            global font_value
            font_value=value
            font_demo.config(font=("Jetbrains Mono",font_value))
            self.editor_font_size=font_value
            self.editor.config(font=("JetBrains Mono",self.editor_font_size))
            self.output.config(font=("JetBrains Mono",self.editor_font_size))

        font_window=Toplevel(self)
        font_window.geometry("300x150")
        font_demo=Label(font_window,text="aAbBcC",font=("JetBrains Mono",font_value))
        font_demo.pack()
        font_slider=Scale(font_window,from_=8,to=50,font=("Poppins SemiBold",10),orient=HORIZONTAL,command=lambda e:font_resizer(value=font_slider.get()))
        font_slider.pack()


    def new(self):
        self.FILE_PATH=''
        self.title(f"Code Editor")
        self.editor.delete("1.0", END)

    def show_status_bar(self):
        if self.status_bar.get()==False:
            self.char_count.config(fg="#FFFFFF")
        else:
            self.char_count.config(fg="#000000")
    def counter(self):
        self.char_count.config(text=f"chars: {len(self.editor.get('1.0',END))}")

    def run(self):
        command = ['python', self.FILE_PATH]
        process = subprocess.Popen(
            args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.output.config(state=NORMAL)
        self.output.insert(END, output.decode("utf-8"),)
        self.output.insert(END,error.decode('utf-8'))
        self.output.config(state=DISABLED)

    def open(self):
        if self.editor.get("1.0", END).rstrip() == '':
            path = askopenfilename(filetypes=[("Python Files", "*.py")])
            with open(path) as file:
                self.editor.insert("1.0", file.read())
            self.FILE_PATH = path
            self.separator = '->' if self.FILE_PATH != '' else ''
            self.title(f"Code Editor{self.separator}{self.FILE_PATH}")
            self.counter()
        else:
            messagebox.showwarning("Warning!", "Please save this file first")


if __name__ == "__main__":
    CodeEditor().mainloop()
