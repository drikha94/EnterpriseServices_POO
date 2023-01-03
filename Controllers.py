from Get_Interface_Data_ import Get_Interface_Data
from Get_Vpn_Data import Get_vpn_data
from Get_Bgp_Data import Get_bgp_data
from Filter_Block import Filter_blocks
from Check_Version import version
from Open_File import open_txt
from Establish_Parameters import parameters
from Get_Routes_data import Get_routes_data
from Get_Possible_Peers import Get_peers_data

class Controller:

    def __init__(self, path, core_interface):

        self.path = path
        self.core_interface = core_interface
        self.core_list = open_txt(self.path)
        self.patterns = version.check_version(self.core_list)
        self.parameters = parameters
        self.possible_peers = []
        self.filter = Filter_blocks()
        self.interface = Get_Interface_Data()
        self.vpn = Get_vpn_data()
        self.routes = Get_routes_data()
        self.peers = Get_peers_data()
        self.bgp = Get_bgp_data()

    def interface_parameters(self):

        block_list = self.filter.interface_filter(self.core_interface, self.core_list)
        self.interface.get_data(self.parameters, block_list, self.patterns)
        #print(self.parameters)

    def vpn_parameters(self):

        if self.parameters['INTER']['VPN'] != "":
            block_list = self.filter.vpn_filter(self.parameters, self.patterns, self.core_list)
            self.vpn.get_data(self.parameters, block_list, self.patterns)
            #print(self.parameters)

    def peers_parameters(self):

        if self.parameters['INTER']['IP'] != "":
            block_list = self.peers.get_data(self.parameters)
            self.possible_peers = block_list

    def routes_parameters(self):

        if self.possible_peers != []:
            block_list = self.filter.routes_filter(self.parameters, self.patterns, self.core_list)
            if block_list != []:
                self.routes.get_data(self.parameters, block_list, self.possible_peers, self.patterns)
        #print(self.parameters)

    def bgp_parameters(self):

        block_list = self.filter.bgp_filter(self.parameters, self.patterns, self.core_list, self.possible_peers)
        print(block_list)
        print(parameters)





path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "GigabitEthernet9/17.2847"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/4/1/16.2746100"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

manager = Controller(path, core_int)
manager.interface_parameters()
manager.vpn_parameters()
manager.peers_parameters()
manager.routes_parameters()
manager.bgp_parameters()




