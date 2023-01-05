from Filter_Blocks.Main_Filter_block import Filter_main_blocks
from Peer_Filter import Select_peer
import re

class Bgp_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
        self.select_peer = Select_peer()
    
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
