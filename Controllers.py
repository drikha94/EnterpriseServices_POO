from Check_Version import version
from Open_File import open_txt, append_txt
from Establish_Parameters import parameters, residential_parameters
from Reset_parameters import reset_establish_parameters, reset_residential_parameters
from tkinter import messagebox
import re

#IMPORTACION DE LOS MODULOS QUE QUE CONTIENEN LOS TEMPLATE
from Templates.Enterprise_Service import *
from Templates.Display_command import *
from Templates.Show_command import *
from Templates.Management import Management_template
from Templates.Residential_Services import Template_residential

#IMPORTACION DE LOS MODULOS QUE REEMPLAZAN LOS DATOS EN LOS TEMPLATE
from Replacement.Replacement_enterprise import Service_template
from Replacement.Replacement_display import Display_template
from Replacement.Replacement_show import Show_template
from Replacement.Replacement_residential import Service_template_res

#IMPORTACION DE LOS MODULOS QUE RETORNAN UN BLOQUE EN ESPECIFICO DEL CORE
from Filter_Blocks.Interface import Interface_filter_block
from Filter_Blocks.Vpn import Vpn_filter_block
from Filter_Blocks.Routes import Routes_filter_block
from Filter_Blocks.Bgp import Bgp_filter_block
from Filter_Blocks.Rip import Rip_filter_block
from Filter_Blocks.Policy import Policy_filter_block
from Filter_Blocks.Route_map import Map_filter_block
from Filter_Blocks.Filter_H4_port import Filter_h4_port
from Filter_Blocks.Filter_residential_data import Filter_residential

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
from Clean_Blocks.Get_H4_Interface_Data import Get_h4_interface_data

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
        self.residential_parameters = residential_parameters
        self.residential_parameters['NEW_INTERFACE_1'] = int_service
        self.parameters = parameters
        self.parameters['NEW_INTERFACE'] = int_service
        self.parameters['CABLING_TYPE'] = cabling_type
        self.parameters['H4_NAME'] = h4_name
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
            block_list = peer.get_data(self.parameters['INTER']['IP'], self.parameters['INTER']['MASK'])
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
        

    def template_management(self, ip_mgmt, device_name, type_cabling, id_service, razon_social):
        self.parameters['MANAGEMENT_DATA']['mgmt_ip'] = ip_mgmt if ip_mgmt != "" else 'X.X.X.X'
        self.parameters['MANAGEMENT_DATA']['device_name'] = device_name if device_name != "" else 'DEVICE_NAME'
        self.parameters['MANAGEMENT_DATA']['ID'] = id_service if id_service != "" else 'ID_NUMBER'
        self.parameters['MANAGEMENT_DATA']['RAZON_SOCIAL'] = razon_social if razon_social != "" else 'RAZON_SOCIAL'
        template_management_obj = Management_template(self.parameters, self.path_script, headers_template)
        self.read_script = open_txt(self.path_script)
        if not re.findall('# ENTERPRISE SERVICE #', "".join(self.read_script)):
            template_management_obj.add_headers()
        
        if self.device_type == 'S2300':
            template_management_obj.switch_mgmt()
        if self.device_type == 'TMARC (UTP)' and self.parameters['CABLING_TYPE'] == 'ELECTRIC':
            template_management_obj.tmarc_electric_mgmt()
        if self.device_type == 'TMARC (FO)' and self.parameters['CABLING_TYPE'] == 'FIBER':
            template_management_obj.tmarc_fiber_mgmt()
        if self.device_type == 'ATN':
            template_management_obj.atn_mgmt()
        if self.device_type == 'CORE':
            template_management_obj.core_mgmt()

    def template_enterprise(self, cabling_type):
        
        template_service_obj = Service_template(self.parameters, self.path_script)
        policy_in = self.parameters['INTER']['POLICY_IN']
        vpn = self.parameters['INTER']['VPN']
    
        template_service_obj.ref_id(ref_id_template)

        if policy_in != "":
            search_policy = [x for x in self.read_script if re.findall(f'traffic behavior {policy_in}', x) and x == f'traffic behavior {policy_in}']
            if search_policy == []:
                template_service_obj.policy_service(policy_template)

        if vpn != "":
            search_vpn = [x for x in self.read_script if re.findall(f'ip vpn-instance {vpn}', x) and x == f'ip vpn-instance {vpn}']
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
        template_service_obj.interface_service(interface_template, cabling_type)
        template_service_obj.routes_service(routes_template)
        template_service_obj.close_txt()

    def template_display(self):

        template_display_obj = Display_template(self.parameters, self.path_display)
        template_display_obj.display_command()
    
    def template_show(self):

        template_display_obj = Show_template(self.parameters, self.path_show, self.patterns)
        template_display_obj.show_command()
    
    def alarm(self):
        if self.parameters['INTER']['VPN'] == "BCOFRANCES":
            messagebox.showwarning("Warning", "The VPN is BCOFRANCES, please check the additional peers")
        if self.parameters['INTER']['IP_SEC'] != "":
            messagebox.showwarning("Warning", "IP sub was detected, please check the configuration")
        if self.parameters['INTER']['IPV6'] != "":
            messagebox.showwarning("Warning", "The service have IPV6, please check")
        if self.parameters['BGP']['ATTRIBUTES']['password cipher'][0] == True and self.parameters['INTER']['VPN'] != 'BCOPATAGONIA':
            messagebox.showwarning("Warning", "The peer have a password, please ask the customer")
    
    def h4_port(self, path, interface):
        self.h4_list = open_txt(path)
        h4_int_obj = Filter_h4_port(self.h4_list, interface)
        clean_h4_int = Get_h4_interface_data()
        block_list = h4_int_obj.interfaces_filter()
        if block_list != []:
            clean_h4_int.get_data(self.parameters, block_list)
        
        print(self.parameters['H4_PORT_STATE'])

    def reset_parameters(self):
        self.parameters = reset_establish_parameters(self.parameters)

    #################################################### RESIDENTIAL FUNTIONS

    def get_residential_data(self, interface_2, id, eth):

        self.residential_parameters['NEW_INTERFACE_2'] = interface_2
        self.residential_parameters['ID'] = id
        self.residential_parameters['NEW_ETH'] = eth
        peers_obj = Get_peers_data()
        get_data_obj = Filter_residential(self.residential_parameters)
        get_data_obj.filter_data(self.core_list, self.core_interface, self.patterns['id'], peers_obj)

    def template_residential(self, device_type):

        template_residential_obj = Template_residential(self.residential_parameters, device_type)
        replacement_obj = Service_template_res(self.residential_parameters, self.path_script)
        self.read_script = open_txt(self.path_script)

        if not re.findall('# RESIDENTIAL SERVICE #', "".join(self.read_script)):
            replacement_obj.write_template(template_residential_obj.headers())

        replacement_obj.write_template(template_residential_obj.headers_service())

        replacement_obj.write_template(template_residential_obj.templates_create_eth())
        replacement_obj.write_template(template_residential_obj.physical_int(self.residential_parameters['NEW_INTERFACE_1']))
        if self.residential_parameters['NEW_INTERFACE_2'] != "":
            replacement_obj.write_template(template_residential_obj.physical_int(self.residential_parameters['NEW_INTERFACE_2']))
        replacement_obj.write_template(template_residential_obj.int_eth())

        if device_type == 'GPON':
            replacement_obj.write_template(template_residential_obj.templates_qos())
        else:
            replacement_obj.write_template(template_residential_obj.add_numeral())

        if self.residential_parameters['VLAN']['TRAFFIC INTERNET'] != []:
            for x in range(len(self.residential_parameters['VLAN']['TRAFFIC INTERNET'])):
                replacement_obj.write_template(template_residential_obj.template_speedy(
                    self.residential_parameters['VLAN']['TRAFFIC INTERNET'][x][0],
                    self.residential_parameters['VLAN']['TRAFFIC INTERNET'][x][1],
                    x
                ))
        
        if self.residential_parameters['VLAN']['TRAFFIC VOIP'] != []:
            for x in range(len(self.residential_parameters['VLAN']['TRAFFIC VOIP'])):
                replacement_obj.write_template(template_residential_obj.voip_template(
                    self.residential_parameters['VLAN']['TRAFFIC VOIP'][x][0],
                    self.residential_parameters['VLAN']['TRAFFIC VOIP'][x][1],
                ))
        
        if self.residential_parameters['VLAN']['GESTION GID1'] != []:
            for x in range(len(self.residential_parameters['VLAN']['GESTION GID1'])):
                replacement_obj.write_template(template_residential_obj.gid_template(
                    self.residential_parameters['VLAN']['GESTION GID1'][x][0],
                    self.residential_parameters['VLAN']['GESTION GID1'][x][1],
                    self.residential_parameters['VLAN']['GESTION GID1'][x][2]
                ))

        if self.residential_parameters['VLAN']['NGN TRAFFIC'] != []:
            for x in range(len(self.residential_parameters['VLAN']['NGN TRAFFIC'])):
                replacement_obj.write_template(template_residential_obj.ngn_traffic_template(
                    self.residential_parameters['VLAN']['NGN TRAFFIC'][x][0],
                    self.residential_parameters['VLAN']['NGN TRAFFIC'][x][1],
                    self.residential_parameters['VLAN']['NGN TRAFFIC'][x][2],
                ))
        
        if self.residential_parameters['VLAN']['NGN SENIALIZATION'] != []:
            for x in range(len(self.residential_parameters['VLAN']['NGN SENIALIZATION'])):
                replacement_obj.write_template(template_residential_obj.ngn_senialization_template(
                    self.residential_parameters['VLAN']['NGN SENIALIZATION'][x][0],
                    self.residential_parameters['VLAN']['NGN SENIALIZATION'][x][1],
                    self.residential_parameters['VLAN']['NGN SENIALIZATION'][x][2],
                ))
        
        if self.residential_parameters['VLAN']['IPTV MULTICAST'] != []:
            for x in range(len(self.residential_parameters['VLAN']['IPTV MULTICAST'])):
                replacement_obj.write_template(template_residential_obj.iptv_multi_template(
                    self.residential_parameters['VLAN']['IPTV MULTICAST'][x][0],
                    self.residential_parameters['VLAN']['IPTV MULTICAST'][x][1],
                    self.residential_parameters['VLAN']['IPTV MULTICAST'][x][2],
                ))
        
        if self.residential_parameters['VLAN']['IPTV UNICAST'] != []:
            for x in range(len(self.residential_parameters['VLAN']['IPTV UNICAST'])):
                replacement_obj.write_template(template_residential_obj.iptv_uni_template(
                    self.residential_parameters['VLAN']['IPTV UNICAST'][x][0],
                    self.residential_parameters['VLAN']['IPTV UNICAST'][x][1],
                    self.residential_parameters['VLAN']['IPTV UNICAST'][x][2],
                    self.residential_parameters['VLAN']['IPTV UNICAST'][x][3],
                ))
        
        if self.residential_parameters['VLAN']['GESTION MODEMS'] != []:
            for x in range(len(self.residential_parameters['VLAN']['GESTION MODEMS'])):
                replacement_obj.write_template(template_residential_obj.modems_template(
                    self.residential_parameters['VLAN']['GESTION MODEMS'][x][0],
                    self.residential_parameters['VLAN']['GESTION MODEMS'][x][1],
                ))
        
        if self.residential_parameters['VLAN']['TRAFFIC ENTERPRISE'] != []:
            for x in range(len(self.residential_parameters['VLAN']['TRAFFIC ENTERPRISE'])):
                replacement_obj.write_template(template_residential_obj.enterprise_template(
                    self.residential_parameters['VLAN']['TRAFFIC ENTERPRISE'][x][0],
                    self.residential_parameters['VLAN']['TRAFFIC ENTERPRISE'][x][1],
                ))
    
    def template_display_res(self):

        template_display_obj = Display_template(self.residential_parameters, self.path_display)
        template_display_obj.display_residential_cmd()

    def reset_parameters_res(self):
        self.parameters = reset_residential_parameters(self.residential_parameters)
    







        

#RESIDENTIAL TEST
"""
path = "C:/Users/awx910701/Documents/Configuraciones/Script/2023/Febrero/Santa Rosa/Old Device/CESRS01.txt"
ce_int = "TenGigabitEthernet4/3"

path_2 = 'C:/Users/awx910701/Documents/Configuraciones/Script/2021/MAYO/Sarandi/Old Device/CESRN02.txt'
ce_int_2 = 'TenGigE0/2/1/0'

work_space = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan"
h4_name = 'H4-SJ-SJN01'

device_type= 'DSLAM'
new_int = '5/5/5'
cabling_type = 'FIBER'

manager = Controller(path, ce_int, work_space, h4_name, device_type, new_int, cabling_type)
manager.get_residential_data()
manager.template_residential()
"""
#ENTERPRISE TEST
"""
path ="C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan/Old Device/CORE-SJN6.gics.ar.telefonica.com-2022-10-31_02_22_09.txt"
core_int = "9/3.341180"

path_v2 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Octubre/Bahia Blanca/Old device/CORE-BHB9.gics.ar.telefonica.com-2022-09-30_02_14_52.txt"
core_int_v2 = "0/4/1/16.140110"

path_v3 = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Junio/Bahia Blanca/Old Device/CORE-BHB7.gics.ar.telefonica.com-2022-06-02_02_14_15.txt"
core_int_v3 = "5/0/5.999"

path_v4 = "C:/Users/awx910701/Documents/Configuraciones/Script/2021/FEBRUARY/Neuquen2/Old Device/CORE-NQN9.gics.ar.telefonica.com-2021-02-11_02_01_41.txt"
core_int_v4 = '0/4/1/0.3395115'

path_v5 = "C:/Users/awx910701/Documents/Configuraciones/Script/2023/Febrero/Santa Rosa/Old Device/CORE-CHV8.gics.ar.telefonica.com-2023-01-27_02_36_17.txt"
core_int_v5 = '7/18.3346101'

work_space = "C:/Users/awx910701/Documents/Configuraciones/Script/2022/Noviembre/San Juan"

h4_name = 'H4-SJ-SJN01'

#get h4 port
path_h4_cfg = 'C:/Users/awx910701/Documents/Configuraciones/Script/2023/Enero/Rada Tilly/Old Device/H4-CB-CRV01.txt'
interface = '8/0/7'

ip_mgmt='10.10.10.10'
device_name = 'prueba'
new_int= '88'
id_service = '5555' 
adred = '77777'
device_type = 'CORE'
cabling_type = 'FIBER'

manager = Controller(path_v5, core_int_v5, work_space, h4_name, device_type, new_int, cabling_type)
manager.interface_parameters()
manager.vpn_parameters()
manager.peers_parameters()
manager.routes_parameters()
manager.bgp_parameters()
manager.rip_parameters()
manager.map_parameters()
manager.prefix_parameters()
manager.policy_parameters()
manager.h4_port(path_h4_cfg, interface)
manager.template_management(ip_mgmt, device_name, cabling_type, id_service, adred)
manager.template_enterprise(cabling_type)
manager.template_display()
manager.template_show()
manager.alarm()
manager.reset_parameters()"""












