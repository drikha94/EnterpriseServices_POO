from io import open
import re

class Get_vpn_data:

    def get_data_v_one(self, parameters, block_list, patterns):

        def get_rd():
        
            parameters['VPN']['RD'] = "".join(filter(lambda x: patterns['vpn']['p_rd'][0] in x, block_list))
            parameters['VPN']['RD'] = parameters['VPN']['RD'].replace(patterns['vpn']['r_rd'][0], "").strip()

        def get_rte():

            parameters['VPN']['RTE'] = "".join(filter(lambda x: patterns['vpn']['p_rte'][0] in x, block_list))            
            parameters['VPN']['RTE'] = parameters['VPN']['RTE'].replace(patterns['vpn']['r_rte'][0], "").strip().split(" ")
            parameters['VPN']['RTE'] = [x for x in parameters['VPN']['RTE'] if x != ""]

        def get_rti():

            parameters['VPN']['RTI'] = "".join(filter(lambda x: patterns['vpn']['p_rti'][0] in x, block_list))
            parameters['VPN']['RTI'] = parameters['VPN']['RTI'].replace(patterns['vpn']['r_rti'][0], "").strip().split(" ")
            parameters['VPN']['RTI'] = [x for x in parameters['VPN']['RTI'] if x != ""]

        def get_description():

            parameters['VPN']['DESCRIP'] = "".join(filter(lambda x: patterns['vpn']['p_descrip'][0] in x,  block_list))
            parameters['VPN']['DESCRIP'] = parameters['VPN']['DESCRIP'].replace(patterns['vpn']['r_descrip'][0], "").strip()

        def get_map():

            parameters['VPN']['MAP'] = "".join(filter(lambda x: patterns['vpn']['p_map'][0] in x, block_list)).strip()

        get_rd(), get_rte(), get_rti(), get_description(), get_map()


    def get_data_v_two(self, parameters, block_list, patterns, data_type):

        def get_rte():

            if data_type == 'rte_block':
                parameters['VPN']['RTE'] = [x.strip() for x in block_list if re.findall(r'\d+:\d+',x)]

        def get_rti():

            if data_type == 'rti_block':
                parameters['VPN']['RTI'] = [x.strip() for x in block_list if re.findall(r'\d+:\d+',x)]

        def get_any():

            if data_type == 'any':
                parameters['VPN']['DESCRIP'] = "".join(filter(lambda x: patterns['vpn']['p_descrip'][0] in x, block_list))
                parameters['VPN']['DESCRIP'] = parameters['VPN']['DESCRIP'].replace(patterns['vpn']['r_descrip'][0], "").strip()

        get_rte(), get_rti(), get_any()
                            

        return parameters

