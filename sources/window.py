import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
from sources.commands import DEFAULT_COUNT,DEFAULT_LENGTH
import typing as t
import sys
import pathlib

class GUI:
    
    PACK_OPTIONS : t.Final[t.Dict[str,int]]={
        'padx':10,   
    }
    
    WINDOW_HEIGHT : t.Final[int]=600
    WINDOW_WIDTH : t.Final[int]=600
    output_path: t.Optional[pathlib.Path]=None
    
    def __init__(self) -> None:
        self.setup_root()
        self.create_widgets()
        self.setup_bindings()
        self.setup_layout()
        

    def setup_root(self):
        self.root=tk.Tk()
        self.root.title("Simple Password Generator")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.iconphoto(False,tk.PhotoImage(file='assets/gpg.png'))
        
        self.root.resizable(False,False)
        
        

          
    def create_widgets(self):
        
        MAX_SCREEN_WIDTH : t.Final[int]=int(self.root.winfo_screenwidth())
        MAX_SCREEN_HEIGHT : t.Final[int]=int(self.root.winfo_screenheight())

        
        self.font=tkfont.Font(root=self.root,family='Ariel',size=14)
        
        
        
        
        CHARACTER_WIDHT : t.Final[int]=self.font.measure('A')
        CHARACTER_HEIGHT : t.Final[int]=self.font.metrics('linespace')
        MAX_LENGTH_SLIDER_WIDTH : t.Final[int]=int(MAX_SCREEN_WIDTH/CHARACTER_WIDHT)
        MAX_COUNT_SLIDER_HEIGHT : t.Final[int]=int(MAX_SCREEN_HEIGHT/CHARACTER_HEIGHT)
        SLIDERS_LENGTH : t.Final[int]=max(MAX_LENGTH_SLIDER_WIDTH,MAX_COUNT_SLIDER_HEIGHT)
        
        
        self.states : dict[str,tk.Variable]={
            'write_to_file': tk.BooleanVar(),
            'length_slider': tk.IntVar(value=DEFAULT_LENGTH),
            "count_slider": tk.IntVar(value=DEFAULT_COUNT),
            'textbox': tk.StringVar(),
        }
        self.widgets : dict[str,tk.Widget]={
            'length_slider':tk.Scale(self.root,from_=1,bigincrement=1,to=MAX_LENGTH_SLIDER_WIDTH,length=SLIDERS_LENGTH,variable=self.states['length_slider'],
                                     orient=tk.HORIZONTAL,label='Length',command=self.on_length_change),
            'count_slider':tk.Scale(self.root,from_=1,bigincrement=1,to=MAX_COUNT_SLIDER_HEIGHT,length=SLIDERS_LENGTH,variable=self.states['count_slider'],
                                    command=self.on_count_change,orient=tk.HORIZONTAL,label='Count'),
            'checkbox':tk.Checkbutton(self.root,text='Write to file',variable=self.states['write_to_file'],command=self.on_checkbox_check),
            'textbox':tk.Text(self.root,height=DEFAULT_COUNT,width=DEFAULT_LENGTH,font=self.font),
            'file_picker':tk.Button(self.root,text='...',command=self.on_file_picker),
            'generate_button':tk.Button(self.root,text='Generate',command=self.on_generate),
            'copy_button': tk.Button(self.root,text='Copy',command=self.on_copy)
            
            
        } 
        
        self.widgets['textbox'].tag_configure(tk.SEL,background='blue',foreground='white')
        
        self.widgets['textbox'].tag_bind(tk.SEL,'<Control-a>',self.highlight_text)
        
        
    def on_generate(self):
        import sources.core as core
        length=self.states['length_slider'].get()
        count=self.states['count_slider'].get()
        passwords=core.generate_passwords(count,length)
        write_to_file=self.states['write_to_file'].get()
        if not(write_to_file):
            self.widgets['textbox'].delete('1.0',tk.END)
            for password in passwords:
                self.widgets['textbox'].insert(tk.END,password+'\n')
            return
        if self.output_path is None:
            return
        
        with open(self.output_path,'w') as file:
            for password in passwords:
                file.write(password+'\n')
            self.disable_generate_button()
            self.output_path=None        
        
        
    def on_file_picker(self):

        file_path=filedialog.asksaveasfilename(title='Save passwords to File',confirmoverwrite=True,defaultextension='.txt')
        if not(file_path):
            self.disable_generate_button()
            return
        file_path=pathlib.Path(file_path)
        self.output_path=file_path
        self.enable_generate_button()
            
        
    def on_copy(self):
        passwords=self.widgets['textbox'].get('1.0',tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(passwords)
        
    def setup_bindings(self):
        # When pressing CTRL+A, select all text in the textbox
        self.widgets['textbox'].bind('<Control-a>',self.highlight_text)
        self.widgets['textbox'].bind('<Key>',lambda a: 'break')
        
    def highlight_text(self,event : tk.Event):
        self.widgets['textbox'].tag_add(tk.SEL,'1.0',tk.END)
        return 'break'
        
    def on_length_change(self,event):
        length_slider=self.states['length_slider'].get()
        # height : t.Final[int]=self.root.winfo_height()
        # new_width=max(self.WINDOW_WIDTH,self.WINDOW_WIDTH+(length_slider*14))
        # self.root.geometry(f"{new_width}x{height}")
        
        self.widgets['textbox'].config(width=length_slider)
        
    def on_count_change(self,event):
        count_slider=self.states['count_slider'].get()
        self.widgets['textbox'].config(height=count_slider)
        
    def hide_text_box(self):
        self.widgets['textbox'].pack_forget()
        
    def show_text_box(self):
        self.widgets['textbox'].pack(**self.PACK_OPTIONS)

    def hide_file_picker(self):
        self.widgets['file_picker'].pack_forget()
        
    def show_file_picker(self):
        self.widgets['file_picker'].pack(**self.PACK_OPTIONS)
        
    def disable_generate_button(self):
        self.widgets['generate_button'].config(state=tk.DISABLED)
        
    def enable_generate_button(self):
        self.widgets['generate_button'].config(state=tk.NORMAL)
        
    def on_checkbox_check(self):
        if self.states['write_to_file'].get():
            self.disable_generate_button()
            self.show_file_picker()
            self.hide_text_box()
            return
            
        self.hide_file_picker()
        self.show_text_box()
        self.enable_generate_button()
        
    def setup_layout(self):

        for widget in self.widgets.values():
            widget.pack(self.PACK_OPTIONS)
        self.widgets['file_picker'].pack_forget()
        
    def run(self):
        self.root.mainloop()
