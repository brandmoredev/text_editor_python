import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *


class TextEditor:
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Text Editor Program")
        self.SCREEN_WIDTH = self.window.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.window.winfo_screenheight()

        #coordinates of top-left corner of the window
        self.x = int((self.SCREEN_WIDTH / 2) - (self.WINDOW_WIDTH / 2))
        self.y = int((self.SCREEN_HEIGHT / 2) - (self.WINDOW_HEIGHT / 2))
        self.window.geometry("{}x{}+{}+{}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.x, self.y))

        #default instance variables
        self.font_name = StringVar(self.window)
        self.font_name.set("Arial")

        self.font_size = StringVar(self.window)
        self.font_size.set("12")

        #text area
        self.text_area = Text(self.window, font=(self.font_name.get(), self.font_size.get()))
        self.text_area.grid(sticky=N + E + S + W)
        self.scroll_bar = Scrollbar(self.text_area, cursor="hand2")
        self.scroll_bar.pack(side=RIGHT,fill=Y)
        self.scroll_bar.config(command=self.text_area.yview) # sync scrollbar movement to text view position
        self.text_area.config(yscrollcommand=self.scroll_bar.set) #sync text view position with scrollbar

        #selected text range
        self.selected_text_range = None

        #bind mouse click release with text area
        self.text_area.bind("<<Selection>>", self.update_selected_text)

        #allows expansion of text_area with respect to window size
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        #WiIDGETS FOR MODIFYING TEXT STYLES
        self.frame = Frame(self.window)
        self.frame.grid()

        #font color
        self.color_button = Button(self.frame, text="color", command=self.change_color)
        self.color_button.grid(row=0,column=0)

        #font
        self.font_name_box = OptionMenu(self.frame, self.font_name, *font.families(), command=self.change_font)
        self.font_name_box.grid(row=0,column=1)

        #font size
        self.font_size_box = Spinbox(self.frame, from_=6, to=100, increment=2, width=6, textvariable=self.font_size, command=self.change_font)
        self.font_size_box.grid(row=0, column=2)

        #MENU OPTIONS
        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        #File Menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        #Edit Menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)

        #Help Menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        help_menu.add_command(label="About", command=self.about)


        #initialize window
        self.window.mainloop()

    def update_selected_text(self, event=None):
        #get range of selected text
        ranges = self.text_area.tag_ranges("sel") 

        if not ranges or len(ranges) < 2:
            self.selected_text_range = None
            return

        #Update self.selected_text_range
        start, end = ranges
        self.selected_text_range = (start, end)

    def change_color(self):
        # Check if there is a valid selection
        if self.selected_text_range:
            tag_name = "selected_text" + str(self.selected_text_range)
            
            # Add the tag to the selected range
            self.text_area.tag_add(tag_name, *self.selected_text_range)

            color = colorchooser.askcolor(title="Select a color")
            self.text_area.tag_config(tag_name, foreground=color[1])

    def change_font(self, *args):
        # Check if there is a valid selection
        if self.selected_text_range:
            tag_name = "selected_text" + str(self.selected_text_range)
            
            # Add the tag to the selected range
            self.text_area.tag_add(tag_name, *self.selected_text_range)
            
            # Configure the tag to apply the font changes
            self.text_area.tag_config(tag_name, font=(self.font_name.get(), self.font_size_box.get()))


    def new_file(self):
        new_editor = TextEditor()
        new_editor.window.title("Untitled")

    def open_file(self):
        file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text Documents", "*.txt")])

        if file:
            try:
                self.window.title(os.path.basename(file.name))

                # Read content from the file and insert it into the new text area
                content = file.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, content)
            except Exception as e:
                showerror("Error", f"Can't open existing file: {e}")
            finally:
                file.close()
                

    def save_file(self):
        pass

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def about(self):
        showinfo("Text Editor", "This text editor is built with Python and Tkinter widgets")

    def quit(self):
        self.window.destroy()

app = TextEditor()




