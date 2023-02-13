from Filter_Blocks.Main_Filter_block import Filter_main_blocks
import re 

class Vpn_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()

    def vpn_filter(self, parameters, patterns, core_list):

        data_type = 'vpn'
        vpn = parameters['INTER']['VPN']

        first_line = list(filter(lambda linea: 'ip vrf ' + vpn in linea, core_list))
        first_line = [x for x in first_line if x == 'ip vrf ' + vpn]

        if first_line == []:
            first_line = list(filter(lambda linea: 'vrf definition ' + vpn in linea, core_list))
        
        if first_line == []:
            first_line = list(filter(lambda linea: 'vrf ' + vpn in linea, core_list))
        
        first_line_filtered = []
        for x in first_line:
            if not re.findall('^ ', x) and re.findall(vpn+'$', x):
                first_line_filtered.append(x)

        block_list = self.main_filter.block(core_list, first_line_filtered, data_type, '!', True, False)

        #if (block_list[0] == patterns['vpn']['p_vpn'][0] + vpn) or (block_list[0] == patterns['vpn']['p_vpn'][1] + vpn):
        if patterns['id'] == 1:
            return block_list

        if patterns['id'] == 2:
            rte_first_line = list(filter(lambda x: patterns['vpn']['p_rte'][0] in x, block_list))
            rti_first_line = list(filter(lambda x: patterns['vpn']['p_rti'][0] in x, block_list))
            rte_block_list = self.main_filter.block(block_list, rte_first_line, data_type, '!', False, False)
            rti_block_list = self.main_filter.block(block_list, rti_first_line, data_type, '!', False, False)
            return [block_list, rte_block_list, rti_block_list]