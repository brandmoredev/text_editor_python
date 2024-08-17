import os
from tkinter import *
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

        #initialize window
        self.window.mainloop()

    def update_selected_text(self, event=None):
        ranges = self.text_area.tag_ranges("sel") #get range of selected text

        if not ranges or len(ranges) < 2:
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
        pass

    def open_file(self):
        pass

    def save_file(self):
        pass

    def cut(self):
        pass

    def copy():
        pass

    def paste():
        pass

    def about():
        pass

    def quit():
        pass

app = TextEditor()




