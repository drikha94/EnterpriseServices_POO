from Check_Version import version
from Open_File import open_txt
from Establish_Parameters import parameters
#from Templates.Management import template_management_obj
from Templates.Bgp import Service_template

"""IMPORTACION DE LOS MODULOS QUE RETORNAN UN BLOQUE EN ESPECIFICO DEL CORE"""
from Filter_Blocks.Interface import Interface_filter_block
from Filter_Blocks.Vpn import Vpn_filter_block
from Filter_Blocks.Routes import Routes_filter_block
from Filter_Blocks.Bgp import Bgp_filter_block
from Filter_Blocks.Policy import Policy_filter_block

"""IMPORTACION DE LOS MODULOS QUE RETORNAN LOS DATOS OBTENIDOS DE LOS BLOQUES"""
from Clean_Blocks.Get_Interface_Data_ import Get_Interface_Data
from Clean_Blocks.Get_Vpn_Data import Get_vpn_data
from Clean_Blocks.Get_Bgp_Data import Get_bgp_data
from Clean_Blocks.Get_Routes_data import Get_routes_data
from Clean_Blocks.Get_Possible_Peers import Get_peers_data
from Clean_Blocks.Get_Traffic_Policy import Get_traffic_policy

class Controller:

    def __init__(self, path, core_interface):

        self.path = path
        self.core_interface = core_interface
        self.core_list = open_txt(self.path)
        self.patterns = version.check_version(self.core_list)
        self.parameters = parameters
        self.possible_peers = []

    def interface_parameters(self):

        interface = Interface_filter_block()
        clean_interface = Get_Interface_Data()
        block_list = interface.interface_filter(self.core_interface, self.core_list)
        clean_interface.get_data(self.parameters, block_list, self.patterns)
        #print(self.parameters)

    def vpn_parameters(self):

        vpn = Vpn_filter_block() 
        clean_vpn = Get_vpn_data()
        if self.parameters['INTER']['VPN'] != "":
            block_list = vpn.vpn_filter(self.parameters, self.patterns, self.core_list)
            clean_vpn.get_data(self.parameters, block_list, self.patterns)

    def peers_parameters(self):

        peer = Get_peers_data()
        if self.parameters['INTER']['IP'] != "":
            block_list = peer.get_data(self.parameters)
            self.possible_peers = block_list

    def routes_parameters(self):

        routes = Routes_filter_block()
        clean_routes = Get_routes_data()
        if self.possible_peers != []:
            block_list = routes.routes_filter(self.parameters, self.patterns, self.core_list, self.possible_peers)
            if block_list != []:
                clean_routes.get_data(self.parameters, block_list, self.patterns)

    def bgp_parameters(self):

        bgp = Bgp_filter_block()
        clean_bgp = Get_bgp_data()
        block_list = bgp.bgp_filter(self.parameters, self.patterns, self.core_list, self.possible_peers)
        if block_list != []:
            clean_bgp.get_data(block_list, self.parameters, self.patterns)

    def policy_parameters(self):

        policy = Policy_filter_block()
        clean_policy = Get_traffic_policy()
        if parameters['INTER']['POLICY_IN'] != "":
            block_list = policy.policy_filter(self.parameters, self.patterns, self.core_list, 'INTER', 'POLICY_IN')
            if block_list != []:
                clean_policy.get_data_policy_in(block_list, self.parameters)

        if parameters['INTER']['POLICY_OUT'] != "" and parameters['INTER']['POLICY_OUT'] != parameters['INTER']['POLICY_IN']:
            block_list = policy.policy_filter(self.parameters, self.patterns, self.core_list, 'INTER', 'POLICY_OUT')
            if block_list != []:
                clean_policy.get_data_policy_out(block_list, self.parameters)

            if parameters['POLICY_OUT']['service-policy'] != "":
                block_list_flow = policy.policy_filter(self.parameters, self.patterns, self.core_list,'POLICY_OUT', 'service-policy')
                if block_list_flow != []:
                    clean_policy.get_data_flow_queue(block_list_flow, self.parameters)


                    

    def template(self):

        template_service_obj = Service_template(self.parameters)
        #print("".join(template_service_obj.bgp_service()))

    

path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "9/17.1729101"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/0/1/7.36610"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

manager = Controller(path_v2, core_int_v2)
manager.interface_parameters()
manager.vpn_parameters()
manager.peers_parameters()
manager.routes_parameters()
manager.bgp_parameters()
manager.policy_parameters()
#manager.template()




