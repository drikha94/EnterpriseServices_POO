import re
from Main_Filter_block import Filter_main_blocks
from Peer_Filter import Select_peer

class Filter_blocks:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
        self.select_peer = Select_peer()
    
    def interface_filter(self, core_interface, core_list):

        data_type = 'interface'
        find_interface = list(filter(lambda linea: core_interface in linea, core_list))
        block_list = self.main_filter.block(core_list, find_interface, data_type, '!', True, False)
        return block_list
    
    def vpn_filter(self, parameters, patterns, core_list):

        data_type = 'vpn'
        vpn = parameters['INTER']['VPN']

        first_line = list(filter(lambda linea: patterns['vpn']['p_vpn'][0] + vpn in linea, core_list))
        if first_line == []:
            first_line = list(filter(lambda linea: patterns['vpn']['p_vpn'][1] + vpn in linea, core_list))
        block_list = self.main_filter.block(core_list, first_line, data_type, '!', True, False)

        if (block_list[0] == patterns['vpn']['p_vpn'][0] + vpn) or (block_list[0] == patterns['vpn']['p_vpn'][1] + vpn):
            if patterns['id'] == 1:
                return block_list

            if patterns['id'] == 2:
                rte_first_line = list(filter(lambda x: patterns['vpn']['p_rte'][0] in x, block_list))
                rti_first_line = list(filter(lambda x: patterns['vpn']['p_rti'][0] in x, block_list))
                rte_block_list = self.main_filter.block(block_list, rte_first_line, data_type, '!', False, False)
                rti_block_list = self.main_filter.block(block_list, rti_first_line, data_type, '!', False, False)
                return [block_list, rte_block_list, rti_block_list]

    def routes_filter(self, parameters, patterns, core_list, peers):

        data_type = 'routes'
        vpn = parameters['INTER']['VPN']

        def add_space(block_list_original):
            block_list = []
            if block_list_original != []:
                for x in block_list_original:
                    block_list.append(f'{x} ')
            return block_list

        if patterns['id'] == 1:

            block_list_original = list(filter(lambda x: 'ip route ' in x, core_list))
            block_list = add_space(block_list_original)

            if vpn != "":
                block_list_reduced = list(filter(lambda x: f'ip route vrf {vpn} ' in x, block_list))
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                block_list_peer = list(filter(lambda x:  f'{peer} ' in x, block_list_reduced)) if peer != "" else []
            else:
                block_list_reduced = list(filter(lambda x: f'ip route' in x if not re.findall('ip route vrf', x) else [], block_list))
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                block_list_peer = list(filter(lambda x:  f'{peer} ' in x, block_list_reduced)) if peer != "" else []
            return block_list_peer

        if patterns['id'] == 2:
            
            block_list = self.main_filter.block(core_list, ['router static'], data_type, '!', True, True)

            if vpn != "":
                first_line = list(filter(lambda x: f'vrf {vpn}' in x, block_list)) if block_list != [] else []
                block_list_reduced = self.main_filter.block(block_list, first_line, data_type, '!', False, False) if first_line != [] else []
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                block_list_peer = list(filter(lambda x:  f'{peer} ' in x, block_list_reduced)) if peer != "" else []
            else:
                block_list_reduced = self.main_filter.block(block_list, block_list, data_type, '!', False, False) if block_list != [] else []
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                block_list_peer = list(filter(lambda x:  f'{peer} ' in x, block_list_reduced)) if peer != "" else []
            return block_list_peer
    
    def bgp_filter(self, parameters, patterns, core_list, peers):

        data_type = 'bgp'
        vpn = parameters['INTER']['VPN']
        first_line = list((filter(lambda x: "router bgp " in x, core_list)))
        block_list = self.main_filter.block(core_list, first_line, data_type, '!', True, True)  if first_line != [] else []

        if vpn == "" and block_list != []:

            if patterns['id'] == 1:
                block_list_reduced = self.main_filter.block(block_list, block_list, data_type, 'address-family ipv4 vrf', False, False)
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                parameters['BGP']['PEER'] = peer
                if peer != "":
                    block_list_peer = list(filter(lambda x: f'{peer} ' in x, block_list_reduced))
                    return block_list_peer
                return []
                
            if patterns['id'] == 2:
                block_list_reduced = self.main_filter.block(block_list, block_list, data_type, 'vrf', False, False)
                peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                parameters['BGP']['PEER'] = peer
                if peer != "":
                    first_line = list(filter(lambda x: f'{peer} ' in x, block_list_reduced))
                    block_list_peer = self.main_filter.block(block_list_reduced, first_line, data_type, ' ! ', True, False)
                    return block_list_peer
                return []

        if vpn != "" and block_list != []:

            if patterns['id'] == 1:
                first_line = list(filter(lambda x: f'address-family ipv4 vrf {vpn} ' in x, block_list))
                if first_line != []:
                    block_list_reduced = self.main_filter.block(block_list, first_line, data_type, '!', False, False)
                    peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                    parameters['BGP']['PEER'] = peer
                    vpn_properties = [x for x in block_list_reduced if not re.findall('neighbor', x)]
                    if peer != "":
                        peer_properties = list(filter(lambda x: f'neighbor {peer} ' in x, block_list_reduced))
                        block_list_peer = peer_properties + vpn_properties
                        return block_list_peer
                    return vpn_properties
                return []

            if patterns['id'] == 2:
                first_line = list(filter(lambda x: f'vrf {vpn} ' in x, block_list))
                if first_line != []:
                    block_list_reduced = self.main_filter.block(block_list, first_line, data_type, ' ! ', True, False)
                    peer = self.select_peer.peer_filter(peers, "".join(block_list_reduced))
                    parameters['BGP']['PEER'] = peer
                    vpn_properties = self.main_filter.block(block_list_reduced, block_list_reduced, data_type, '! ', False, False)
                    if peer != "":
                        first_line_peer = list(filter(lambda x: f'neighbor {peer} ' in x, block_list_reduced))
                        peer_properties = self.main_filter.block(block_list_reduced, first_line_peer, data_type, '! ', False, False)   
                        return peer_properties + vpn_properties
                    return vpn_properties
                return []

    def policy_filter(self, parameters, patterns, core_list, policy_type):

        data_type = 'traffic_policy'
        policy = parameters['INTER'][policy_type]
        first_line = list(filter(lambda x: f'policy-map {policy}' in x, core_list))
        if first_line != []:
            block_list = self.main_filter.block(core_list, first_line, data_type, '!', True, False)
            block_list.remove(block_list[0])
            block_list.remove(block_list[len(block_list) - 1])
            return block_list
        else:
            return []




        
       




            


            



        
                    
        