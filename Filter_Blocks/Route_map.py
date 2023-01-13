from Filter_Blocks.Main_Filter_block import Filter_main_blocks
import re

class Map_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
    
    def map_filter(self, parameters, patterns, core_list, map):
        
        data_type = 'route_map'
        if map == 'in':
            map = parameters['BGP']['ATTRIBUTES']['route-policy_in'][1] 
        if map == 'out':
            map = parameters['BGP']['ATTRIBUTES']['route-policy_out'][1]

        if patterns['id'] == 1:

            find_map = list((filter(lambda x: f"route-map {map} " in x, core_list)))

            block_list = []
            map_filtered = []
            for x in find_map:
                if not re.findall('^ ', x):
                    map_filtered.append(x)

            for x in range(len(map_filtered)):
                if map_filtered != []:
                    block_list.append(self.main_filter.block(core_list, [map_filtered[x]], data_type, '!', False, False))

        if patterns['id'] == 2:

            pass

        
        return block_list