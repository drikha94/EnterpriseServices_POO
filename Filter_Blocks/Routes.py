
from Filter_Blocks.Main_Filter_block import Filter_main_blocks
from Peer_Filter import Select_peer
import re

class Routes_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
        self.select_peer = Select_peer()

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