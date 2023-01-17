from Filter_Blocks.Main_Filter_block import Filter_main_blocks
import re

class Map_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()
    
    def map_filter(self, parameters, patterns, core_list, map_in_out):
        
        data_type = 'route_map'
        if map_in_out == 'in':
            map = parameters['BGP']['ATTRIBUTES']['route-policy_in'][1]
        if map_in_out == 'out':
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
            
            find_map = list((filter(lambda x: f"route-policy {map}" in x, core_list)))
            block_list = []
            map_filtered = []

            for x in find_map:
                if not re.findall('^ ', x):
                    map_filtered.append(x)
            
            map_filtered = [x for x in map_filtered if x == f'route-policy {map}']
            if map_filtered != []:
                block_list.append(self.main_filter.block(core_list, map_filtered, data_type, '!', False, False))
        
        return block_list