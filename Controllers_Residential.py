from Open_File import open_txt
from Establish_Parameters_res import parameters
from Filter_residential_data import Filter_residential


class Controller_residential:

    def __init__(self, ce_cfg, ce_int):

        self.ce_cfg = open_txt(ce_cfg)
        self.ce_int = ce_int
        self.parameters = parameters
        self.version = 1 if "".join(filter(lambda x: "address-family ipv4 vrf" in x, self.ce_cfg)) != "" else ""
        self.version = 2 if "".join(filter(lambda x: "router static" in x, self.ce_cfg)) != "" else self.version

    def get_data(self):

        get_data_obj = Filter_residential(self.parameters)
        get_data_obj.filter_data(self.ce_cfg, self.ce_int, self.version)
        print(self.parameters)


path = "C:/Users/awx910701/Documents/Configuraciones/Script/2023/Febrero/Santa Rosa/Old Device/CESRS01.txt"
ce_int = "TenGigabitEthernet4/3"

path_2 = 'C:/Users/awx910701/Documents/Configuraciones/Script/2021/MAYO/Sarandi/Old Device/CESRN02.txt'
ce_int_2 = 'TenGigE0/2/1/0'

manager = Controller_residential(path, ce_int)
manager.get_data()

