from tkinter import *
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
from String_Methods import *
import subprocess


class CodeEditor(Tk):
    editor_font_size = 20

    def __init__(self):
        super().__init__()
        self.FILE_PATH = ''
        self.separator = ': ' if self.FILE_PATH != '' else ''
        self.title(f"Code Editor{self.separator}{self.FILE_PATH}")
        self.state("zoomed")
        self.iconbitmap("./code editor.ico")

        # main frame
        self.main_frame = Frame(self)
        self.main_frame.pack()

        
        # main menu
        self.main_menu = Menu(self)
        # self.main_menu.configure(tearoff=0)
        self.first_menu = Menu(self.main_menu, tearoff=0)
        self.first_menu.add_command(
            label=space_between("New File", "Ctrl+N", 30), command=self.new)
        self.first_menu.add_command(label=space_between(
            "Open File", "Ctrl+O", 30), command=self.open)
        self.recent_files = Menu(self.first_menu, tearoff=0)
        self.first_menu.add_separator()
        self.first_menu.add_command(label=space_between(
            "Save", "Ctrl+S", 30), command=self.save)
        self.first_menu.add_command(label=space_between(
            "Run", "Ctrl+B", 30), command=self.run)
        self.main_menu.add_cascade(menu=self.first_menu, label="File")

        self.main_window = PanedWindow(
            self.main_frame, orient=VERTICAL, sashpad=2)
        # code editor
        self.editor = Text(
            self.main_window,
            width=self.winfo_screenwidth(),
            height=20,
            font=("jetbrains mono", self.editor_font_size),
        )

        self.editor.pack()
        #Run Button
        self.shadow_button=Button(self.main_frame,bg="#757575",borderwidth=0,text="Run",font=("Poppins SemiBold",10),state=DISABLED)
        self.shadow_button.place(x=1473,y=7)
        self.run_button=Button(self.main_frame,text="Run",command=self.run,borderwidth=0,font=("Poppins SemiBold",10))
        self.run_button.place(x=1470,y=4)
        self.editor.bind("<Control-s>", self.save)
        self.editor.bind("<Control-o>", self.open)
        self.editor.bind("<Control-n>", self.new)
        # self.editor.bind("<Control-s>", self.save)
        self.main_window.add(self.editor)
        self.config(menu=self.main_menu)

        self.output = Text(
            self.main_window,
            width=self.winfo_screenwidth(),
            height=5,
            font=("jetbrains mono", self.editor_font_size),
            state=DISABLED,
        )
        self.output.pack()
        self.main_window.add(self.output)
        self.main_window.pack(fill=BOTH, expand=1)
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

    def new(self):
        self.FILE_PATH=''
        self.title(f"Code Editor")
        self.editor.delete("1.0", END)

    def run(self):
        command = ['python', self.FILE_PATH]
        process = subprocess.Popen(
            args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.output.config(state=NORMAL)
        self.output.insert("1.0", output.decode("utf-8"),)
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
        else:
            messagebox.showwarning("Warning!", "Please save this file first")


if __name__ == "__main__":
    CodeEditor().mainloop()
