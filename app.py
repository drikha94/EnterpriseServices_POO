from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import os
import re
from Controllers import Controller

class Main_aplicacion:

    def __init__(self, root):

        self.root = root
        self.root.title("Script Generator")
        self.root.resizable(False,False)
        self.root.config(relief="ridge", background="black")
        self.frame_main()
        self.images()
        self.button()
        self.tags()
        self.styles()
        self.listbox()

        
    def frame_main(self):   
        
        self.myframe=Frame(self.root)
        self.myframe.grid(row = 0, column = 0, padx=15, pady=15)
        self.myframe.config(width="70", height="50", background="#252525")
        self.myframe_two=Frame(self.root)
        self.myframe_two.grid(row = 1, column = 0, padx=15, pady=15)
        self.myframe_two.config(width="70", height="50", background="#252525")
        self.lb_fm = LabelFrame(self.myframe, text='Add Path', bg='#252525', fg='#597EE3')
        self.lb_fm.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def button(self):

        ttk.Button(self.myframe, text="Enterprise", width=17, style = "TButton", command=self.insert_enterprise_list).grid(row=2, column=0, padx=(10,5), pady=5)
        ttk.Button(self.myframe, text="Residential", width=17, style = "TButton", command=self.insert_residential_list).grid(row=3, column=0, padx=(10,5), pady=5)
        ttk.Button(self.myframe, text="Mobile", width=17, style = "TButton", command=self.insert_mobile_list).grid(row=4, column=0, padx=(10,5), pady=5)
        ttk.Button(self.lb_fm, width=5, style = "TButton", image=self.txt_image, command=self.open_file).grid(row=0, column=2, padx=(10,10), pady=(0,5))
        ttk.Button(self.lb_fm, width=5, style = "TButton", image=self.dir_image, command=self.open_dir).grid(row=1, column=2, padx=(10,10), pady=(0,5))
        ttk.Button(self.lb_fm, text="Continue", width=28, style = "TButton", command=self.button_enterprises_services).grid(row=1, column=0, columnspan=2, padx=(15,5), pady=(0,0))
        Entry(self.lb_fm, width=15, justify=CENTER, highlightcolor="#597EE3", highlightbackground="#C8C8C8", highlightthickness=1, background='#252525', fg='#B9B4C3').grid(row=0, column=1, padx=(10,5))
        Label(self.lb_fm, text='H4 NAME', background='#252525', foreground='#B9B4C3').grid(column=0, row=0, padx=10)
    
    def open_file(self):

        core_path = ""
        core_path = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))
        print(core_path)
    
    def open_dir(self):

        work_space = ""
        work_space = filedialog.askdirectory()
        print(work_space)
    
    def listbox(self):

        self.scrollbar = ttk.Scrollbar(self.myframe, orient=VERTICAL, style="TScrollbar")
        self.listbox = Listbox(self.myframe, 
                        borderwidth=0,  
                        highlightcolor="#597EE3",
                        highlightbackground="#597EE3",
                        bg = "#5E5B5B", 
                        fg='#C8C8C8', 
                        selectbackground="#597EE3",
                        height=6,
                        width=16,
                        yscrollcommand=self.scrollbar.set)
        self.listbox.grid(column=1, row=2, rowspan=3, padx=20, pady=5)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.place(relx=0.91, rely=0.23, width=13, height=99)

    def insert_enterprise_list(self):
        
        self.listbox.delete(0,END)
        self.listbox.insert(0, 'S2300')
        self.listbox.insert(END, 'TMARC (FO)','TMARC (UTP)', 'ATN', 'CORE', 'DSLAM')
    
    def insert_residential_list(self):
        
        self.listbox.delete(0,END)
        self.listbox.insert(0, 'DSLAM')
        self.listbox.insert(END, 'GPON')
    
    def insert_mobile_list(self):
        
        self.listbox.delete(0,END)
        self.listbox.insert(0, 'RBS')
        self.listbox.insert(END, 'ATN')
    

    def tags(self):
        self.l_two = Label(self.myframe, text="SCRIPT PROCESS", background="#252525", fg= "#B9B4C3")
        self.l_two.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.l_one = Label(self.myframe, text="TYPE OF SERVICE", background="#252525", fg= "#B9B4C3")
        self.l_one.grid(row=1, column=0, pady=5, padx=5)
        self.l_two = Label(self.myframe, text="SELECT DEVICE", background="#252525", fg= "#B9B4C3")
        self.l_two.grid(row=1, column=1, pady=5, padx=5)
    
    def images(self):
        
        absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
        absolute_image_path = os.path.join(absolute_folder_path, 'txt_image8.png')
        absolute_image_path_two = os.path.join(absolute_folder_path, 'open_dir8.png')
        self.txt_image = PhotoImage(file=absolute_image_path)
        self.dir_image = PhotoImage(file=absolute_image_path_two)
        self.txt_image = self.txt_image.subsample(20)
        self.dir_image = self.dir_image.subsample(30)
    
    def button_enterprises_services(self):

        selection = self.listbox.curselection()
        if selection != ():
            get_device = self.listbox.get(selection[0])
            self.top = Toplevel(bg = "black", padx=10, pady=10)
            self.fm_one_top = Frame(self.top, bg = "#252525", pady=5, padx=5)
            self.fm_one_top.grid(row=0,column=0, sticky=W)

            if get_device == 'S2300':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=5)
                Label(self.fm_one_top, text="Loopback193", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                Label(self.fm_one_top, text="S2300 Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                Label(self.fm_one_top, text="ID (Path)", background="#252525", fg= "#C8C8C8").grid(column=0, row=3, padx=5)
                Label(self.fm_one_top, text="Adred", background="#252525", fg= "#C8C8C8").grid(column=0, row=4, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525')
                self.e_top_one.grid(column=1, row=1, padx=5, pady=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_tree.grid(column=1, row=3, padx=5, pady=5)
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_four.grid(column=1, row=4, padx=5, pady=5)

            if get_device == 'ATN':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=5)
                Label(self.fm_one_top, text="H5 Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                Label(self.fm_one_top, text="ID (Path)", background="#252525", fg= "#C8C8C8").grid(column=0, row=3, padx=5)
                Label(self.fm_one_top, text="Adred", background="#252525", fg= "#C8C8C8").grid(column=0, row=4, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525')
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_tree.grid(column=1, row=3, padx=5, pady=5)
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_four.grid(column=1, row=4, padx=5, pady=5)
            
            if get_device == 'TMARC (FO)':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=10)
                Label(self.fm_one_top, text="IP Mgmt", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                Label(self.fm_one_top, text="Tmarc Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525')
                self.e_top_one.grid(column=1, row=1, padx=5, pady=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')

            if get_device == 'TMARC (UTP)':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=10)
                Label(self.fm_one_top, text="Tmarc Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525')
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_two.grid(column=1, row=1, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525')

            Label(self.fm_one_top, text="Service data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=5, columnspan=2, pady=5)
            Label(self.fm_one_top, text="*" ,background="#252525", fg= "#922121", font=('20')).grid(column=1, row=5, columnspan=3, pady=5)
            Label(self.fm_one_top, text="Old interface", background="#252525", fg= "#C8C8C8").grid(column=0, row=6, padx=5, pady=5)
            Label(self.fm_one_top, text="New interface", background="#252525", fg= "#C8C8C8").grid(column=0, row=7, padx=5, pady=5)
            Entry(self.fm_one_top, width=14, highlightcolor="red",highlightbackground="#C8C8C8",highlightthickness=1, background='#252525').grid(column=1, row=6, padx=5, pady=5)
            Entry(self.fm_one_top, width=14, highlightcolor="red",highlightbackground="#C8C8C8",highlightthickness=1, background='#252525').grid(column=1, row=7, padx=5, pady=5)
            ttk.Button(self.fm_one_top, text="Start", width=13, style='TButton', command=self.script_generator).grid(column=0, row=8, pady=15, padx=5)
            ttk.Button(self.fm_one_top, text="Delete all", width=13, style='TButton').grid(column=1, row=8, pady=15, padx=5)

            return self.e_top_one, self.e_top_two, self.e_top_tree, self.e_top_four

    
    def script_generator(self):
        ip_mgmt = self.e_top_one.get()
        name_service = self.e_top_two.get()
        id = self.e_top_tree.get()
        adred = self.e_top_four.get()

        print(adred)
        
            
        #manager_ctls = Controller(path, core_int, work_space, h4_name, device_type, new_int, cabling_type)

    def tags_box(self):

        el_one = Label(self.myframe, text="Old Interface:", background="#474343", fg= "#B9B4C3")
        el_one.grid(row=1, column=0)
        el_two = Label(self.myframe, text="New Interface:", background="#474343", fg= "#B9B4C3")
        el_two.grid(row=2, column=0)
        el_tree = Label(self.myframe, text="ID Red (Path):", background="#474343", fg= "#B9B4C3")
        el_tree.grid(row=3, column=0)
        el_four = Label(self.myframe, text="Adred-Adecir:", background="#474343", fg= "#B9B4C3")
        el_four.grid(row=4, column=0)
        el_five = Label(self.myframe, text="LoopBack193:", background="#474343", fg= "#B9B4C3")
        el_five.grid(row=5, column=0)
        el_six = Label(self.myframe, text="Service Name:", background="#474343", fg= "#B9B4C3")
        el_six.grid(row=6, column=0)
        el_seven = Label(self.myframe, text="------------------------------------------", background="#474343", fg= "#B9B4C3")
        el_seven.grid(row=8, column=0, columnspan=2)
    
    def text_box(self):

        box_one = Entry(self.myframe, width=15)
        box_one.grid(row=1, column=1, padx=5, pady=5)
        box_two = Entry(self.myframe, width=15)
        box_two.grid(row=2, column=1, padx=5, pady=5)
        box_tree = Entry(self.myframe, width=15)
        box_tree.grid(row=3, column=1, padx=5, pady=5)
        box_four = Entry(self.myframe, width=15)
        box_four.grid(row=4, column=1, padx=5, pady=5)
        box_five = Entry(self.myframe,width=15)
        box_five.grid(row=5, column=1, padx=5, pady=5)
        box_sex = Entry(self.myframe,width=15)
        box_sex.grid(row=6, column=1, padx=5, pady=5)
        box_seven = Entry(self.myframe, width=15)
        box_seven.grid(row=9, column=0, padx=5, pady=5)
        box_eich = Entry(self.myframe, width=15)
        box_eich.grid(row=9, column=1, padx=5, pady=5)


    def styles(self):

        style = ttk.Style()

        style.configure("TButton", 
            foreground="black", 
            background = "#597EE3", 
            activeforeground="red",
            relief="flat", 
            borderwidth = 0, 
            overrelief="flat-raised"),
        style.map(
            "TButton", 
            foreground = [('pressed', 'black'), ('active', 'black')], 
            background = [('pressed', '!disabled', '#5E5B5B'), ('active', '#5E5B5B')],)

        style.configure(
            "TScrollbar",
            arrowcolor="black",
            background="gray",
            troughcolor="#597EE3")
        style.map(
            'TScrollbar',
            background = [('pressed', '!disabled', 'gray'), ('active', '#545755')],
        )
    
    def destroy_main_windowns(self):

        self.l_one.destroy()
        self.b_one.destroy() 
        self.b_two.destroy()
        self.b_tree.destroy()
        self.b_get_ip.destroy()
        self.b_get_mac.destroy()
        self.l_two.destroy()
        self.b_automation.destroy()
        self.l_tree.destroy()
    
    def destroy_enterprise_winfowns(self):
        
        self.l_one.destroy()
        self.b_s2300.destroy()
        self.b_tmarc.destroy()
        self.b_atn.destroy()
        self.b_ip_transit.destroy()
        self.b_core.destroy()
        self.b_dslam.destroy()
        self.b_automation.destroy()


if __name__ == "__main__":
	root = Tk()
	app = Main_aplicacion(root)
	root.mainloop()