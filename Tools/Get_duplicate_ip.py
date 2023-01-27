import re
import os
from tkinter import messagebox

def open_txt(path):

    configuration_path = path
    text = open(configuration_path, "r")
    text_to_list = list(map(str.rstrip, text))
    text.close()
    return text_to_list

class Duplicate_ip:

    def __init__(self, path_h4, path_script):

        self.path_h4 = path_h4 
        self.path_script = path_script
        self.config_h4 = open_txt(path_h4)
        self.config_script = open_txt(path_script)
    
    def get_data(self):

        self.h4_list_interface, self.script_list_interface = [], []
        
        def get_first_line(config_to_read, list_to_append):
            for x in config_to_read:
                if re.findall(r'^interface', x):
                    list_to_append.append(x)

        get_first_line(self.config_h4, self.h4_list_interface), get_first_line(self.config_script, self.script_list_interface)

    def get_ip_and_vpn(self):

        self.h4_dict = {}
        self.script_dict = {}

        def get_h4(dict, lista, cfg):

            for x in range(len(lista)):
                dict[x] = ["", "", ""]
                indice = cfg.index(lista[x])
                dict[x][0] = lista[x]

                for i in range(indice, len(cfg)):
                    if re.findall('ip binding vpn-instance', cfg[i]):
                        dict[x][1] = cfg[i].replace('ip binding vpn-instance', "").strip()

                    if re.findall(r'ip address ', cfg[i]):
                        dict[x][2] = re.findall(r'ip address ', cfg[i])
                        dict[x][2] = cfg[i].replace(r'ip address ', "").strip().split()
                        dict[x][2] = dict[x][2][0]
                        break

                    if re.findall('#', cfg[i]):
                        break

        get_h4(self.h4_dict, self.h4_list_interface, self.config_h4)
        get_h4(self.script_dict, self.script_list_interface, self.config_script)
    
    def compare(self):

        self.duplicate_ip = []
        for x in range(len(self.script_dict)):
            ip_conf, vpn_conf = self.script_dict[x][2], self.script_dict[x][1]
            for i in range(len(self.h4_dict)):
                ip_h4, vpn_h4 = self.h4_dict[i][2], self.h4_dict[i][1]
                if ip_conf == ip_h4 and vpn_conf == vpn_h4:
                    if self.script_dict[x][2] != "":
                        list_combo = []
                        list_combo.append(self.script_dict[x][0])
                        list_combo.append(self.script_dict[x][1])
                        list_combo.append(self.script_dict[x][2])
                        self.duplicate_ip.append(list_combo)
    
    def generate_message(self):

        mess = []
        for x in range(len(self.duplicate_ip)):
            ip = self.duplicate_ip[x][2]
            vpn = self.duplicate_ip[x][1]
            message = f"""La IP: {self.duplicate_ip[x][2]}, VPN: {self.duplicate_ip[x][1]}\n"""
            mess.append(message)

        if mess != []:
            messagebox.showwarning('Warning', mess)
        else:
            messagebox.showwarning('Warning', 'There are not duplicate IP')




"""
path_script = 'C:/Users/awx910701/Documents/Configuraciones/Script/2023/Enero/Rada Tilly/CFG_H4-CB-RTL01.txt'
path_h4 = 'C:/Users/awx910701/Documents/Configuraciones/Script/2023/Enero/Rada Tilly/H4-CB-RTL01_.txt'
check_ip = Duplicate_ip(path_h4, path_script)
check_ip.get_data()
check_ip.get_ip_and_vpn()
check_ip.compare()
check_ip.generate_message() """

