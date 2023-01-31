from Open_File import open_txt
from Establish_Parameters_res import parameters
from Filter_residential_data import Filter_residential


class Controller_residential:

    def __init__(self, ce_cfg, ce_int):

        self.ce_cfg = open_txt(ce_cfg)
        self.ce_int = ce_int
        self.parameters = parameters

    def get_data(self):

        get_data_obj = Filter_residential(self.parameters)
        get_data_obj.filter_data(self.ce_cfg, self.ce_int)
        print(self.parameters)






path = "C:/Users/awx910701/Documents/Configuraciones/Script/2023/Febrero/Santa Rosa/Old Device/CESRS01.txt"
ce_int = "GigabitEthernet9/13"

manager = Controller_residential(path, ce_int)
manager.get_data()

