from Check_Version import version
from Open_File import open_txt, append_txt
from Establish_Parameters import parameters
from Reset_parameters import reset_establish_parameters
import re

#IMPORTACION DE LOS MODULOS QUE QUE CONTIENEN LOS TEMPLATE
from Templates.Enterprise_Service import *
from Templates.Display_command import *
from Templates.Show_command import *
from Templates.Management import Management_template

#IMPORTACION DE LOS MODULOS QUE REEMPLAZAN LOS DATOS EN LOS TEMPLATE
from Replacement.Replacement_enterprise import Service_template
from Replacement.Replacement_display import Display_template
from Replacement.Replacement_show import Show_template

#IMPORTACION DE LOS MODULOS QUE RETORNAN UN BLOQUE EN ESPECIFICO DEL CORE
from Filter_Blocks.Interface import Interface_filter_block
from Filter_Blocks.Vpn import Vpn_filter_block
from Filter_Blocks.Routes import Routes_filter_block
from Filter_Blocks.Bgp import Bgp_filter_block
from Filter_Blocks.Rip import Rip_filter_block
from Filter_Blocks.Policy import Policy_filter_block
from Filter_Blocks.Route_map import Map_filter_block

#IMPORTACION DE LOS MODULOS QUE RETORNAN LOS DATOS OBTENIDOS DE LOS BLOQUES
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

    def __init__(self, path, core_interface, work_space, h4_name, device_type, int_service, cabling_type):

        self.path = path
        self.core_interface = core_interface
        self.core_list = open_txt(self.path)
        self.core_name = "".join(filter(lambda x: "hostname " in x, self.core_list)).replace('hostname ', '').strip()
        self.path_script = work_space + f'/CFG_{h4_name}_SCRIPT.txt'
        self.path_display = f'{work_space}/CML_{h4_name}_POSTCHECK.txt'
        self.path_show = f'{work_space}/CML_{self.core_name}_PRECHECK.txt'
        self.patterns = version.check_version(self.core_list)
        self.parameters = parameters
        self.parameters['NEW_INTERFACE'] = int_service
        self.parameters['CABLING_TYPE'] = cabling_type
        self.possible_peers = []
        self.device_type = device_type

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
        if self.parameters['BGP']['ATTRIBUTES']['route-policy_in'][0] == True:
            block_list = map.map_filter(self.parameters, self.patterns, self.core_list, 'in')
            if block_list != []:
                self.parameters['ROUTE_MAP_IN']['route_policy_quantity'] = len(block_list)
                for x in range(len(block_list)):
                    clean_map.get_data(block_list[x], self.parameters, self.patterns, 'ROUTE_MAP_IN')

        if self.parameters['BGP']['ATTRIBUTES']['route-policy_out'][0] == True:
            block_list = map.map_filter(self.parameters, self.patterns, self.core_list, 'out')
            if block_list != []:
                self.parameters['ROUTE_MAP_OUT']['route_policy_quantity'] = len(block_list)
                for x in range(len(block_list)):
                    clean_map.get_data(block_list[x], self.parameters, self.patterns, 'ROUTE_MAP_OUT')
        
    def prefix_parameters(self):

        clean_prefix = Get_prefix_data()

        if self.parameters['ROUTE_MAP_IN']['match ip address prefix-list'] != []:
            clean_prefix.get_data(self.parameters, self.patterns, self.core_list, 'in')
        
        if self.parameters['ROUTE_MAP_OUT']['match ip address prefix-list'] != []:
            clean_prefix.get_data(self.parameters, self.patterns, self.core_list, 'out')

    def policy_parameters(self):

        policy = Policy_filter_block()
        clean_policy = Get_traffic_policy()
        if self.parameters['INTER']['POLICY_IN'] != "":
            block_list = policy.policy_filter(self.parameters, self.core_list, 'INTER', 'POLICY_IN')
            if block_list != []:
                clean_policy.get_data_policy_in(block_list, self.parameters)

        if self.parameters['INTER']['POLICY_OUT'] != "" and self.parameters['INTER']['POLICY_OUT'] != self.parameters['INTER']['POLICY_IN']:
            block_list = policy.policy_filter(self.parameters, self.core_list, 'INTER', 'POLICY_OUT')
            if block_list != []:
                clean_policy.get_data_policy_out(block_list, self.parameters)

            if self.parameters['POLICY_OUT']['service-policy'] != "":
                block_list_flow = policy.policy_filter(self.parameters, self.core_list,'POLICY_OUT', 'service-policy')
                if block_list_flow != []:
                    clean_policy.get_data_flow_queue(block_list_flow, self.parameters)
        

    def template_management(self, ip_mgmt, device_name, type_cabling, id_service, adred):
        self.parameters['MANAGEMENT_DATA']['mgmt_ip'] = ip_mgmt if ip_mgmt != "" else 'X/X/X'
        self.parameters['MANAGEMENT_DATA']['device_name'] = device_name if device_name != "" else 'DEVICE_NAME'
        self.parameters['MANAGEMENT_DATA']['ID'] = id_service if id_service != "" else 'ID_NUMBER'
        self.parameters['MANAGEMENT_DATA']['ADRED'] = adred if adred != "" else 'ADRED_NUMBER'
        read_script = open_txt(self.path_script)
        template_management_obj = Management_template(self.parameters, self.path_script, headers_template)
        if not re.findall('# ENTERPRISE SERVICE #', "".join(open_txt(self.path_script))):
            template_management_obj.add_headers()
        if self.device_type == 'S2300':
            template_management_obj.switch_mgmt()
        if self.device_type == 'TMARC' and self.parameters['CABLING_TYPE'] == 'ELECTRIC':
            template_management_obj.tmarc_electric_mgmt()
        if self.device_type == 'TMARC' and self.parameters['CABLING_TYPE'] == 'FIBER':
            template_management_obj.tmarc_fiber_mgmt()
        if self.device_type == 'ATN':
            template_management_obj.atn_mgmt()
        if self.device_type == 'CORE':
            template_management_obj.core_mgmt()

    def template_enterprise(self, type):

        template_service_obj = Service_template(self.parameters, self.path_script)
        policy_in = self.parameters['INTER']['POLICY_IN']
        vpn = self.parameters['INTER']['VPN']
        read_script = open_txt(self.path_script)

        if not re.findall('# ENTERPRISE SERVICE #', "".join(read_script)):
            template_service_obj.headers(headers_template)
        
        template_service_obj.ref_id(ref_id_template)

        if policy_in != "":
            search_policy = [x for x in read_script if re.findall(f'traffic behavior {policy_in}', x) and x == f'traffic behavior {policy_in}']
            if search_policy == []:
                template_service_obj.policy_service(policy_template)

        if vpn != "":
            search_vpn = [x for x in read_script if re.findall(f'ip vpn-instance {vpn}', x) and x == f'ip vpn-instance {vpn}']
            if search_vpn == []:
                template_service_obj.vpn_service(vpn_template)
    
        template_service_obj.prefix_service()

        if self.parameters['BGP']['ATTRIBUTES']['route-policy_in'][0] == True:
            for x in range(self.parameters['ROUTE_MAP_IN']['route_policy_quantity']):
                template_service_obj.map_service(policy_map_template, x, 'in')

        if self.parameters['BGP']['ATTRIBUTES']['route-policy_out'][0] == True:
            for x in range(self.parameters['ROUTE_MAP_OUT']['route_policy_quantity']):
                template_service_obj.map_service(policy_map_template, x, 'out')

        template_service_obj.rip_service(rip_template)
        template_service_obj.bgp_service(bgp_template)
        template_service_obj.flow_service(flow_template)
        template_service_obj.interface_service(interface_template, type)
        template_service_obj.routes_service(routes_template)
        template_service_obj.close_txt()

    def template_display(self):

        template_display_obj = Display_template(self.parameters, self.path_display, display_template)
        template_display_obj.display_command()
    
    def template_show(self):

        template_display_obj = Show_template(self.parameters, self.path_show, self.patterns)
        template_display_obj.show_command()
    
    def reset_parameters(self):
        self.parameters = reset_establish_parameters(self.parameters)


    
path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "9/3.83210"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/4/1/16.140110"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

path_v4 = "C:/Users/awx910701/Documents/Configuraciones/Script/2021/FEBRUARY/Neuquen2/Old Device/CORE-NQN9.gics.ar.telefonica.com-2021-02-11_02_01_41.txt"
core_int_v4 = '0/4/1/0.3395115'

work_space = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan"

h4_name = 'H4-SJ-SJN01'


"""
ip_mgmt='10.10.10.10'
device_name = 'prueba'
new_int= '8/8/8'
id_service = '5555' 
adred = '77777'
device_type = 'S2300'

manager = Controller(path, core_int, work_space, h4_name, device_type, new_int, self.parameters['CABLING_TYPE'])
manager.interface_parameters()
manager.vpn_parameters()
manager.peers_parameters()
manager.routes_parameters()
manager.bgp_parameters()
manager.rip_parameters()
manager.map_parameters()
manager.prefix_parameters()
manager.policy_parameters()
manager.template_management(ip_mgmt, device_name, type_cabling, id_service, adred)
manager.template_enterprise(self.parameters['CABLING_TYPE'])
manager.template_display()
manager.template_show()
manager.reset_parameters()"""








