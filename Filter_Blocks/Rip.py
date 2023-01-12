from Filter_Blocks.Main_Filter_block import Filter_main_blocks
from Peer_Filter import Select_peer
import re

class Rip_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
        self.select_peer = Select_peer()
    
    def rip_filter(self, parameters, patterns, core_list):
        
        data_type = 'rip'
        vpn = parameters['INTER']['VPN']
        old_interface = parameters['OLD_INTERFACE']

        block_list_reduced = []
        first_line = list((filter(lambda x: "router rip" in x, core_list)))
        block_list = self.main_filter.block(core_list, first_line, data_type, '!', True, True)  if first_line != [] else []

        if patterns['id'] == 1 and block_list != []:

            find_vpn = list((filter(lambda x: f" address-family ipv4 vrf {vpn} " in x, block_list)))
            if find_vpn != []:
                block_list_reduced = self.main_filter.block(block_list, find_vpn, data_type, '!', False, False)

        if patterns['id'] == 2 and block_list != []:

            find_vpn = list((filter(lambda x: f" vrf {vpn} " in x, block_list)))
            if find_vpn != []:
                block_list_reduced = self.main_filter.block(block_list, find_vpn, data_type, ' ! ', True, False)
                interface_validation = list((filter(lambda x: f'{old_interface} ' in x, block_list_reduced)))
                if interface_validation == []:
                    block_list_reduced = []

        return block_list_reduced
