from Get_Interface_Data_ import Get_Interface_Data
from Get_Vpn_Data import Get_vpn_data
from Get_Bgp_Data import Get_bgp_data
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
        self.block_routes = ""

    def interface_parameters(self):

        data_type = 'interface'
        find_interface = list(filter(lambda linea: self.core_interface in linea, self.core_list))
        block_list = filter_block(self.core_list, find_interface, data_type, '!')
        interface = Get_Interface_Data()
        interface.get_data(self.parameters, block_list, self.patterns)

    def vpn_parameters(self):

        data_type = 'vpn'
        vpn = self.parameters['INTER']['VPN']

        first_line = list(filter(lambda linea: self.patterns['vpn']['p_vpn'][0] + vpn in linea, self.core_list))
        if first_line == []:
            first_line = list(filter(lambda linea: self.patterns['vpn']['p_vpn'][1] + vpn in linea, self.core_list))

        if vpn != "":

            block_list = filter_block(self.core_list, first_line, data_type, '!')
            if (block_list[0] == self.patterns['vpn']['p_vpn'][0] + vpn) or (block_list[0] == self.patterns['vpn']['p_vpn'][1] + vpn):

                if self.patterns['id'] == 1:

                    vpn_obj = Get_vpn_data()
                    vpn_obj.get_data_v_one(self.parameters, block_list, self.patterns)

                if self.patterns['id'] == 2:

                    rte_first_line = list(filter(lambda x: self.patterns['vpn']['p_rte'][0] in x, block_list))
                    rti_first_line = list(filter(lambda x: self.patterns['vpn']['p_rti'][0] in x, block_list))
                    rte_block_list = filter_block(block_list, rte_first_line, data_type, '  !')
                    rti_block_list = filter_block(block_list, rti_first_line, data_type, '  !')
                    vpn_obj = Get_vpn_data()
                    vpn_obj.get_data_v_two(self.parameters, block_list, self.patterns, 'any')
                    vpn_obj.get_data_v_two(self.parameters, rte_block_list, self.patterns, 'rte_block')
                    vpn_obj.get_data_v_two(self.parameters, rti_block_list, self.patterns, 'rti_block')

    def routes_parameters(self):

        data_type = 'routes'
        first_line = list(filter(lambda x: self.patterns['routes']['p_routes'][0] in x, self.core_list))

        if self.patterns['id'] == 1:
            self.block_routes = first_line

        if self.patterns['id'] == 2:
            block_list = filter_block(self.core_list, first_line, data_type, '!')
            self.block_routes = block_list

    def bgp_parameters(self):

        data_type = 'bgp_one'
        vpn = self.parameters['INTER']['VPN']
        first_line = list((filter(lambda x: "router bgp " in x, self.core_list)))
        block_list = filter_block(self.core_list, first_line, data_type, '!')  if first_line != [] else []

        data_type = 'bgp_two'
        bgp_obj = Get_bgp_data()
        confirmation = bgp_obj.first_filter(self.parameters, block_list, self.patterns)
        bgp_obj.get_possible_peers(self.parameters)

        bgp_without_vpn_block = filter_block(block_list, confirmation, data_type, 'vrf') if block_list != [] else []
        if confirmation != False and self.parameters['INTER']['VPN'] != '':
            bgp_with_vpn_block = filter_block(block_list, confirmation, data_type, '!')
            bgp_obj.get_bgp_with_vpn(self.parameters, bgp_with_vpn_block)

        bgp_obj.get_routes_with_vpn(self.parameters, self.block_routes)
        
   
        #bgp_obj.get_data_with_vpn()
        #bgp_obj.get_data_without_vpn()


        #print(bgp_vpn_block)
            #bgp_obj = Get_bgp_data()
            #bgp_obj.get_data(self.parameters, bgp_vpn_block, self.block_routes)
        #print(block_list)
        #print(self.parameters)




path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "GigabitEthernet9/17.1729101"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/0/1/15.4040"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

manager = Controller(path, core_int)
manager.interface_parameters()
manager.vpn_parameters()
manager.routes_parameters()
manager.bgp_parameters()




