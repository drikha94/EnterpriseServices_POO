from Get_Interface_Data_ import Get_Interface_Data
from Filter_Block import filter_block
from Check_Version import version
from Open_File import open_txt
from Establish_Parameters import parameters

class Controller:

    def __init__(self, path, core_interface):

        self.path = path
        self.core_interface = core_interface
        self.core_list = open_txt(self.path)
        self.patterns = version.check_version(self.core_list)
        self.parameters = parameters

    def interface_parameters(self):

        data_type = 'interface'
        find_interface = list(filter(lambda linea: self.core_interface in linea, self.core_list))
        block_list = filter_block(self.core_list, find_interface, data_type)
        interface = Get_Interface_Data()
        interface.get_data(self.parameters, block_list, self.patterns)
        #print(self.parameters)

    def vpn_parameters(self):

        data_type = 'vpn'
        vpn = self.parameters['INTER']['VPN']
        first_line = list(filter(lambda linea: self.patterns['vpn']['p_vpn'][0] + vpn in linea, self.core_list))
        if first_line == []:
            first_line = list(filter(lambda linea: self.patterns['vpn']['p_vpn'][1] + vpn in linea, self.core_list))
        block_list = filter_block(self.core_list, first_line, data_type)
        if block_list[0] == self.patterns['vpn']['p_vpn'][0] + vpn:
            pass
        print(block_list)




path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "GigabitEthernet12/12.3411200"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/0/1/15.4040"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

manager = Controller(path_v3, core_int_v3)
manager.interface_parameters()
manager.vpn_parameters()




