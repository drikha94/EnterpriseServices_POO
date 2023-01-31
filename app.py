from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import os
import re
from Controllers import Controller
from Tools.Get_duplicate_ip import Duplicate_ip
from Tools.Get_Mac_CML import Mac_address_cml

class Main_aplicacion:

    def __init__(self, root):

        self.root = root
        self.root.title("Script Generator")
        self.root.resizable(False,False)
        self.root.config(relief="ridge", background="black")
        self.frame_main()
        self.images()
        self.button_main()
        self.tags()
        self.styles()
        self.listbox()
        self.core_path = ""
        self.work_space = ""
        self.path_h4 = ""
        self.path_script = ""
        self.path_core_mac = ""
        self.path_script_mac = ""
        self.tools_frame()

        
    def frame_main(self):   
        
        self.myframe=Frame(self.root)
        self.myframe.grid(row = 0, column = 0, padx=(10, 5), pady=10)
        self.myframe.config(width="70", height="50", background="#252525")
        self.myframe_two=Frame(self.root)
        self.myframe_two.grid(row = 0, column = 1, padx=(5,10), pady=10)
        self.myframe_two.config(width="70", height="50", background="#252525")
        self.lb_fm = LabelFrame(self.myframe, text='Add Path', bg='#252525', fg='#597EE3')
        self.lb_fm.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.lb_fm_tw = LabelFrame(self.myframe_two, text='Get duplicate IP', bg='#252525', fg='#597EE3')
        self.lb_fm_tw.grid(row=1, column=0, padx=5, pady=5)
        self.lb_fm_tree = LabelFrame(self.myframe_two, text='Get Mac-Address CML', bg='#252525', fg='#597EE3')
        self.lb_fm_tree.grid(row=2, column=0, padx=10, pady=10)

    def button_main(self):

        ttk.Button(self.myframe, text="Enterprise", width=17, style = "TButton", command=self.insert_enterprise_list).grid(row=2, column=0, padx=(10,5), pady=5)
        ttk.Button(self.myframe, text="Residential", width=17, style = "TButton", command=self.insert_residential_list).grid(row=3, column=0, padx=(10,5), pady=5)
        ttk.Button(self.myframe, text="Mobile", width=17, style = "TButton", command=self.insert_mobile_list).grid(row=4, column=0, padx=(10,5), pady=5)
        ttk.Button(self.lb_fm, width=5, style = "TButton", image=self.txt_image, command=self.open_file).grid(row=0, column=2, padx=(10,10), pady=(0,5))
        ttk.Button(self.lb_fm, width=5, style = "TButton", image=self.dir_image, command=self.open_dir).grid(row=1, column=2, padx=(10,10), pady=(0,5))
        ttk.Button(self.lb_fm, text="Continue", width=28, style = "TButton", command=self.button_enterprises_services).grid(row=1, column=0, columnspan=2, padx=(15,5), pady=(0,0))
        self.e_main_cero = Entry(self.lb_fm, width=15, justify=CENTER, highlightcolor="#597EE3", highlightbackground="#C8C8C8", highlightthickness=1, background='#252525', fg='#B9B4C3')
        self.e_main_cero.grid(row=0, column=1, padx=(10,5))
        Label(self.lb_fm, text='H4 NAME', background='#252525', foreground='#B9B4C3').grid(column=0, row=0, padx=10)
    
    def open_file(self):

        self.core_path = ""
        self.core_path = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))
    
    def open_dir(self):

        self.work_space = ""
        self.work_space = filedialog.askdirectory()
    
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
        self.scrollbar.place(relx=0.92, rely=0.24, width=13, height=98)

    def insert_enterprise_list(self):
        
        self.listbox.delete(0,END)
        self.listbox.insert(0, 'S2300')
        self.listbox.insert(END, 'TMARC (FO)','TMARC (UTP)', 'ATN', 'CORE', 'NO MGMT')
    
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

        self.selection = self.listbox.curselection()
        if self.core_path == "" or self.work_space == "" or self.selection == () or self.e_main_cero.get() == "":
            messagebox.showinfo("Warning", "Type of device, directory, legacy configuration path and H4 name can't be empty")

        if self.selection != () and self.core_path != "" and self.work_space != "" and self.e_main_cero.get():
            self.get_device = self.listbox.get(self.selection[0])
            self.top = Toplevel(bg = "black", padx=10, pady=10)
            self.top.grab_set()
            self.top.focus_set()
            self.top.resizable(False,False)
            self.fm_one_top = Frame(self.top, bg = "#252525", pady=5, padx=5)
            self.fm_one_top.grid(row=0,column=0, sticky=W)

            if self.get_device == 'S2300':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=5)
                Label(self.fm_one_top, text="Loopback193", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                Label(self.fm_one_top, text="S2300 Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                Label(self.fm_one_top, text="ID (Path)", background="#252525", fg= "#C8C8C8").grid(column=0, row=3, padx=5)
                Label(self.fm_one_top, text="Adred", background="#252525", fg= "#C8C8C8").grid(column=0, row=4, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525', fg= "#C8C8C8")
                self.e_top_one.grid(column=1, row=1, padx=5, pady=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_tree.grid(column=1, row=3, padx=5, pady=5)
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_four.grid(column=1, row=4, padx=5, pady=5)

            if self.get_device == 'ATN':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=5)
                Label(self.fm_one_top, text="H5 Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                Label(self.fm_one_top, text="ID (Path)", background="#252525", fg= "#C8C8C8").grid(column=0, row=3, padx=5)
                Label(self.fm_one_top, text="Adred", background="#252525", fg= "#C8C8C8").grid(column=0, row=4, padx=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)
                self.e_top_tree = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_tree.grid(column=1, row=3, padx=5, pady=5)
                self.e_top_four = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_four.grid(column=1, row=4, padx=5, pady=5)
            
            if self.get_device == 'TMARC (FO)':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=10)
                Label(self.fm_one_top, text="IP Mgmt", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                Label(self.fm_one_top, text="Tmarc Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=2, padx=5)
                self.e_top_one = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, bg='#252525', fg= "#C8C8C8")
                self.e_top_one.grid(column=1, row=1, padx=5, pady=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525',fg= "#C8C8C8")
                self.e_top_two.grid(column=1, row=2, padx=5, pady=5)

            if self.get_device == 'TMARC (UTP)':
                Label(self.fm_one_top, text="Management data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=0, columnspan=3, pady=10)
                Label(self.fm_one_top, text="Tmarc Name", background="#252525", fg= "#C8C8C8").grid(column=0, row=1, padx=5)
                self.e_top_two = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightthickness=1, background='#252525', fg= "#C8C8C8")
                self.e_top_two.grid(column=1, row=1, padx=5, pady=5)

            Label(self.fm_one_top, text="Service data" ,background="#252525", fg= "#C8C8C8").grid(column=0, row=5, columnspan=2, pady=5)
            Label(self.fm_one_top, text="*" ,background="#252525", fg= "#922121", font=('20')).grid(column=1, row=5, columnspan=3, pady=5)
            Label(self.fm_one_top, text="Old interface", background="#252525", fg= "#C8C8C8").grid(column=0, row=6, padx=5, pady=5)
            Label(self.fm_one_top, text="New interface", background="#252525", fg= "#C8C8C8").grid(column=0, row=7, padx=5, pady=5)
            self.e_top_five = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightbackground="#C8C8C8",highlightthickness=1, background='#252525',fg= "#C8C8C8")
            self.e_top_five.grid(column=1, row=6, padx=5, pady=5)
            self.e_top_six = Entry(self.fm_one_top, width=14, highlightcolor="red",highlightbackground="#C8C8C8",highlightthickness=1, background='#252525', fg= "#C8C8C8")
            self.e_top_six.grid(column=1, row=7, padx=5, pady=5)
            ttk.Button(self.fm_one_top, text="Start", width=28, style='TButton', command=self.script_generator).grid(column=0, row=8, columnspan=2,pady=15, padx=5)

            if self.get_device == 'S2300':
                return self.e_top_one, self.e_top_two, self.e_top_tree, self.e_top_four,self.e_top_five, self.e_top_six
            if self.get_device == 'ATN':
                return self.e_top_two, self.e_top_tree, self.e_top_four,self.e_top_five, self.e_top_six
            if self.get_device == 'TMARC (FO)':
                return self.e_top_one, self.e_top_two, self.e_top_five, self.e_top_six
            if self.get_device == 'TMARC (UTP)':
                return self.e_top_two, self.e_top_five, self.e_top_six
            if self.get_device == 'CORE' or 'NO MGMT':
                return self.e_top_five, self.e_top_six

    def script_generator(self):
        h4_name = self.e_main_cero.get().strip()
        cabling_type = 'FIBER'
        name_service = 'DEVICE_NAME'
        id = 'ID_NUMBER'
        adred = 'ADRED_NUMBER'
        ip_mgmt = 'X.X.X.X'

        if self.get_device == 'S2300':
            ip_mgmt = self.e_top_one.get().strip()
            name_service = self.e_top_two.get().strip()
            id = self.e_top_tree.get().strip()
            adred = self.e_top_four.get().strip()
            old_int = self.e_top_five.get().strip()
            new_int = self.e_top_six.get().strip()

        if self.get_device == 'ATN':
            id = self.e_top_tree.get().strip()
            adred=self.e_top_four.get().strip()
            name_service = self.e_top_two.get().strip()
            old_int = self.e_top_five.get().strip()
            new_int = self.e_top_six.get().strip()

        if self.get_device == 'TMARC (FO)':
            ip_mgmt = self.e_top_one.get().strip()
            name_service = self.e_top_two.get().strip()
            old_int = self.e_top_five.get().strip()
            new_int = self.e_top_six.get().strip()

        if self.get_device == 'TMARC (UTP)':
            name_service = self.e_top_two.get().strip()
            old_int = self.e_top_five.get().strip()
            new_int = self.e_top_six.get().strip()
            cabling_type = 'ELECTRIC'

        if self.get_device == 'CORE' or 'NO MGMT':
            old_int = self.e_top_five.get().strip()
            new_int = self.e_top_six.get().strip()

        if old_int == "" or new_int == "":
            messagebox.showinfo("Warning", "Old and new interface can't be empty")
        else:
            manager_ctls = Controller(self.core_path, old_int, self.work_space, h4_name, self.get_device, new_int, cabling_type)
            manager_ctls.interface_parameters()
            manager_ctls.vpn_parameters()
            manager_ctls.peers_parameters()
            manager_ctls.routes_parameters()
            manager_ctls.bgp_parameters()
            manager_ctls.rip_parameters()
            manager_ctls.map_parameters()
            manager_ctls.prefix_parameters()
            manager_ctls.policy_parameters()
            manager_ctls.template_management(ip_mgmt, name_service, cabling_type, id, adred)
            manager_ctls.template_enterprise(cabling_type)
            manager_ctls.template_display()
            manager_ctls.template_show()
            manager_ctls.alarm()
            manager_ctls.reset_parameters()

            messagebox.showinfo("successful", "The configuration was created successfully")
            continuar = messagebox.askquestion("Cotinue", "Do you want continue with another service?")
            if continuar == "no":
                self.root.destroy()
            else:
                self.top.destroy()
    
    def tools_frame(self):

        Label(self.myframe_two, text='TOOLS', background="#252525", fg= "#B9B4C3").grid(column=0, row= 0, columnspan=2, pady=5)
        ttk.Button(self.lb_fm_tw, width=15, style = "TButton", text='H4 Config.', command=self.get_h4_path_dup).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.lb_fm_tw, width=15, style = "TButton", text='Script Config.', command=self.get_script_path_dup).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.lb_fm_tw, width=35, style = "TButton", text='Continue', command=self.get_duplicate_ip).grid(row=5, column=0,padx=10, pady=10, columnspan=2)
        ttk.Button(self.lb_fm_tree, width=15, style = "TButton", text='CORE Config', command=self.get_core_path_mac).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.lb_fm_tree, width=15, style = "TButton", text='Script file', command=self.get_script_path_mac).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.lb_fm_tree, width=35, style = "TButton", text='Continue', command=self.get_mac_address_cml).grid(row=5, column=0,padx=10, pady=10, columnspan=2)

    def get_h4_path_dup(self):
        self.path_h4 = ""
        self.path_h4 = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))
    
    def get_core_path_mac(self):
        self.path_core_mac = ""
        self.path_core_mac = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))

    def get_script_path_dup(self):
        self.path_script = ""
        self.path_script = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))
    
    def get_script_path_mac(self):
        self.path_script_mac = ""
        self.path_script_mac = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("txt files","*.txt"), ("all files", "*.*")))
    
    
    def get_duplicate_ip(self):
        if self.path_script != "" and self.path_h4 != "":
            check_ip = Duplicate_ip(self.path_h4, self.path_script)
            check_ip.get_data()
            check_ip.get_ip_and_vpn()
            check_ip.compare()
            check_ip.generate_message()
        else:
            messagebox.showinfo('Warning', 'Please add the script and H4 path')
    
    def get_mac_address_cml(self):
        if self.path_core_mac != "" and self.path_script_mac:
            cml = Mac_address_cml(self.path_core_mac, self.path_script_mac)
            cml.mac_address()
            cml.add_to_script()
        else:
            messagebox.showinfo('Warning', 'Please add the script and CORE path')

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
    


if __name__ == "__main__":
	root = Tk()
	app = Main_aplicacion(root)
	root.mainloop()