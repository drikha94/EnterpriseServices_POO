import pandas as pd
import numpy as np
import os
from Controllers import Controller

class Read_workspace:

    def __init__(self, work_space):

        self.workspace = work_space
        self.files_workspace = os.listdir(self.workspace)
        self.subdir = [x for x in self.files_workspace if os.path.isdir(f'{self.workspace}/{x}') == True]
        self.xlsx_files = list(filter(lambda x: '.xlsx' in x, self.files_workspace))
    
    def search_excel_file(self):

        if self.xlsx_files != []:
            for file in self.xlsx_files:
                xls = pd.ExcelFile(f'{self.workspace}/{file}')
                sheets = xls.sheet_names
                b2b_sheets = "".join(filter(lambda x: 'B2B_SERVICES' in x, sheets))
                if b2b_sheets != "":
                    try:
                        df = pd.read_excel(f'{self.workspace}/{file}', sheet_name='B2B_SERVICES')
                        break
                    except PermissionError:
                        print('Please close the excel file, the other way can not read it')
                        break
                else:
                    print('There is not excel file in your workspace whit the sheetname "B2B_ENTERPRISE"')
                return None
            return df
        else:
            print('There is not excel file in your workspace')
    
    def filter_df(self):
        get_df = self.search_excel_file()
        sheet_to_list = []
        
        filter_column = get_df[['TYPE', 'CABLING','DEVICE-NAME','H4-NAME','H4-INT', 'CORE-NAME', 'CORE-INT', 'ID', 'ADRED', 'L193']]
        print(filter_column)

        """
        try:
            filter_column = get_df[['TYPE', 'CABLING','DEVICE-NAME','H4-NAME','H4-INT', 'CORE-NAME', 'CORE-INT', 'ID', 'ADRED', 'L193']]
            sheet_to_list = filter_column.to_numpy().tolist()
            index = [0,1,2,3,4,5,6,7,8,9]
            for i in range(len(index)):
                for x in range(len(sheet_to_list)):
                    value = str(sheet_to_list[x][index[i]])
                    if value != 'nan':
                        only_interface = value
                    sheet_to_list[x][index[i]] = only_interface
        except TypeError:
            pass

        return sheet_to_list"""

    def open_legacy_device(self):

        services_list = self.filter_df()
        print(services_list)
        if services_list != []:
            for core_name in services_list:
                core_configuration = f'{core_name[5].strip()}.gics.ar.telefonica.com'
                core_file = list(filter(lambda x: core_configuration in x , self.files_workspace))

                if core_file != []:
                    path_core = f'{self.workspace}/{core_file[0]}'
                    call_controller(
                                path_core, 
                                core_name[6].strip(), 
                                self.workspace, 
                                core_name[3].strip(),
                                core_name[0].strip(),
                                core_name[9].strip(),
                                core_name[2].strip(),
                                core_name[4].strip(),
                                core_name[0].strip(),
                                core_name[7].strip(),
                                core_name[8].strip(),
                                core_name[1].strip()
                                )

                else:
                    for subdir in self.subdir:
                        sub_files = os.listdir(f'{self.workspace}/{subdir}')
                        core_file = list(filter(lambda x: core_configuration in x , sub_files))
                        if core_file != []:
                            path_core = f'{self.workspace}/{subdir}/{core_file[0]}'
                            call_controller(
                                path_core, 
                                core_name[6].strip(), 
                                self.workspace, 
                                core_name[3].strip(), 
                                core_name[0].strip(),
                                core_name[9].strip(),
                                core_name[2].strip(),
                                core_name[4].strip(),
                                core_name[0].strip(),
                                core_name[7].strip(),
                                core_name[8].strip(),
                                core_name[1].strip()
                                )

            
def call_controller(path, core_int, work_space, h4_name, type_device, ip_mgmt, device_name, new_int, type, id, adred, cabling_type):
    manager_auto = Controller(path, core_int, work_space, h4_name, type_device, new_int, cabling_type)
    manager_auto.interface_parameters()
    manager_auto.vpn_parameters()
    manager_auto.peers_parameters()
    manager_auto.routes_parameters()
    manager_auto.bgp_parameters()
    manager_auto.rip_parameters()
    manager_auto.map_parameters()
    manager_auto.prefix_parameters()
    manager_auto.policy_parameters()
    manager_auto.template_management(ip_mgmt, device_name, type, id, adred)
    manager_auto.template_enterprise(cabling_type)
    manager_auto.template_display()
    manager_auto.template_show()
    manager_auto.reset_parameters()




path_workspace = 'C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/Viedma 2'
workspace = Read_workspace(path_workspace)
#print(workspace.search_excel_file())
print(workspace.filter_df())
#workspace.open_legacy_device()

