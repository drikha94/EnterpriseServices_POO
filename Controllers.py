from Check_Version import version
from Open_File import open_txt
from Establish_Parameters import parameters
from Templates.Replacement import Service_template
from Templates.Enterprise_Service import *

"""IMPORTACION DE LOS MODULOS QUE RETORNAN UN BLOQUE EN ESPECIFICO DEL CORE"""
from Filter_Blocks.Interface import Interface_filter_block
from Filter_Blocks.Vpn import Vpn_filter_block
from Filter_Blocks.Routes import Routes_filter_block
from Filter_Blocks.Bgp import Bgp_filter_block
from Filter_Blocks.Rip import Rip_filter_block
from Filter_Blocks.Policy import Policy_filter_block
from Filter_Blocks.Route_map import Map_filter_block

"""IMPORTACION DE LOS MODULOS QUE RETORNAN LOS DATOS OBTENIDOS DE LOS BLOQUES"""
from Clean_Blocks.Get_Interface_Data_ import Get_Interface_Data
from Clean_Blocks.Get_Vpn_Data import Get_vpn_data
from Clean_Blocks.Get_Bgp_Data import Get_bgp_data
from Clean_Blocks.Get_Rip_Data import Get_rip_data
from Clean_Blocks.Get_Routes_data import Get_routes_data
from Clean_Blocks.Get_Possible_Peers import Get_peers_data
from Clean_Blocks.Get_Traffic_Policy import Get_traffic_policy
from Clean_Blocks.Get_Map_Data import Get_map_data
from Clean_Blocks.Get_Prefix_Data import Get_prefix_data

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
        block_list = interface.interface_filter(self.core_interface, self.core_list, self.parameters)
        clean_interface.get_data(self.parameters, block_list, self.patterns)

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
                if self.parameters['RIP']['network'] or self.parameters['RIP']['neighbor'] != []:
                    self.parameters['RIP']['STATUS'] = True

    def bgp_parameters(self):

        bgp = Bgp_filter_block()
        clean_bgp = Get_bgp_data()
        block_list = bgp.bgp_filter(self.parameters, self.patterns, self.core_list, self.possible_peers)
        if block_list != []:
            self.parameters['BGP']['STATUS'] = True
            clean_bgp.get_data(block_list, self.parameters, self.patterns)
            #print(self.parameters)
    
    def rip_parameters(self):

        if self.parameters['BGP']['ATTRIBUTES']['import-route rip'][0] == True:
            rip = Rip_filter_block()
            clean_rip = Get_rip_data()
            block_list = rip.rip_filter(self.parameters, self.patterns, self.core_list)
            if block_list != []:
                clean_rip.get_data(block_list, self.parameters, self.patterns) 
                self.parameters['RIP']['STATUS'] = True
    
    def map_parameters(self):

        map = Map_filter_block()
        clean_map = Get_map_data()
        if self.parameters['BGP']['ATTRIBUTES']['route-policy_in'][0] != "":
            block_list = map.map_filter(self.parameters, self.patterns, self.core_list, 'in')
            if block_list != []:
                self.parameters['ROUTE_MAP_IN']['route_policy_quantity'] = len(block_list)
                for x in range(len(block_list)):
                    clean_map.get_data(block_list[x], self.parameters, self.patterns, self.core_list, 'ROUTE_MAP_IN')

        if self.parameters['BGP']['ATTRIBUTES']['route-policy_out'][0] != "":
            block_list = map.map_filter(self.parameters, self.patterns, self.core_list, 'out')
            if block_list != []:
                self.parameters['ROUTE_MAP_OUT']['route_policy_quantity'] = len(block_list)
                for x in range(len(block_list)):
                    clean_map.get_data(block_list[x], self.parameters, self.patterns, self.core_list, 'ROUTE_MAP_OUT')
        
    def prefix_parameters(self):

        prefix = Get_prefix_data()
        if self.parameters['ROUTE_MAP_IN']['match ip address prefix-list'] != []:
            prefix.get_data(self.parameters, self.patterns, self.core_list, 'in')
        
        if self.parameters['ROUTE_MAP_OUT']['match ip address prefix-list'] != []:
            prefix.get_data(self.parameters, self.patterns, self.core_list, 'out')

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
        if self.parameters['INTER']['POLICY_IN'] != "":
            print("".join(template_service_obj.policy_service(policy_template)))

        if self.parameters['INTER']['VPN'] != "":
            print("".join(template_service_obj.vpn_service(vpn_template)))
        
        if self.parameters['IP_PREFIX'] != []:
            print(("".join(template_service_obj.prefix_service())))
        
        if self.parameters['BGP']['ATTRIBUTES']['route-policy_in'][0] == True:
            for x in range(self.parameters['ROUTE_MAP_IN']['route_policy_quantity']):
                print("".join(template_service_obj.map_service(policy_map_template, x, 'in')))
        
        if self.parameters['BGP']['ATTRIBUTES']['route-policy_out'][0] == True:
            for x in range(self.parameters['ROUTE_MAP_OUT']['route_policy_quantity']):
                print("".join(template_service_obj.map_service(policy_map_template, x, 'out')))
    
        if self.parameters['RIP']['STATUS'] == True:
            print("".join(template_service_obj.rip_service(rip_template)))

        if self.parameters['BGP']['STATUS'] == True:
            print("".join(template_service_obj.bgp_service(bgp_template)))

        if self.parameters['INTER']['POLICY_OUT'] != "" and self.parameters['INTER']['POLICY_OUT'] != self.parameters['INTER']['POLICY_IN']:
            print("".join(template_service_obj.flow_service(flow_template)))

        print("".join(template_service_obj.interface_service(interface_template, 'fiber')))

        if self.parameters['ROUTES'] != []:
            print("".join(template_service_obj.routes_service(routes_template)))
        
        #print(self.parameters)

path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "9/3.83210"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/4/1/16.338"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

path_v4 = "C:/Users/awx910701/Documents/Configuraciones/Script/2021/FEBRUARY/Neuquen2/Old Device/CORE-NQN9.gics.ar.telefonica.com-2021-02-11_02_01_41.txt"
core_int_v4 = '0/4/1/0.3395115'

manager = Controller(path, core_int)
manager.interface_parameters()
manager.vpn_parameters()
manager.peers_parameters()
manager.routes_parameters()
manager.bgp_parameters()
manager.rip_parameters()
manager.map_parameters()
manager.prefix_parameters()
manager.policy_parameters()
manager.template()




