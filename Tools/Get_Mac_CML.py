import re
from tkinter import messagebox

def open_txt(path):

    configuration_path = path
    text = open(configuration_path, "r")
    text_to_list = list(map(str.rstrip, text))
    text.close()
    return text_to_list

class Mac_address_cml:

    def __init__(self, core_path, script_path):
        self.core_path = open_txt(core_path)
        self.script_path = script_path
        self.vpn_list = []

    def mac_address(self):

        self.vpn_list.append('################# Get Mac-Address CML\n')
        self.vpn_list.append('#\n')
        self.vpn_list.append('show arp\n')
        self.vpn_list.append('show arp dynamic\n')

        for x in self.core_path:

            x = x + '\n'
            if re.findall(r'^vrf definition ', x):
                x = x.replace('vrf definition', 'show arp vrf')
                self.vpn_list.append(x)

            if re.findall(r'^ip vrf ', x):
                x = x.replace('ip vrf', 'show arp vrf')
                self.vpn_list.append(x)

            if re.findall(r'^vrf ', x):
                x = x.replace('vrf', 'show arp vrf')
                self.vpn_list.append(x)
    
    def add_to_script(self):

        open_script = open(self.script_path, "a")
        for x in self.vpn_list:
            open_script.write(x)
        
        open_script.close()
        messagebox.showinfo('Info', 'The command line was added successfully')
        

"""
core_path = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
script_path = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/mac_cml_prueba.txt"

core_path_2 = 'C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt'
script_path = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/mac_cml_prueba.txt"

cml = Mac_address_cml(core_path, script_path)
cml.mac_address()
cml.add_to_script()
"""

