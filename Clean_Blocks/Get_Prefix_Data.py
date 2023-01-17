import re

class Get_prefix_data:

    def get_data(self, parameters, patterns, core_list, in_out):

        if in_out == 'in':
            main_key = 'ROUTE_MAP_IN'
            
        if in_out == 'out':
            main_key = 'ROUTE_MAP_OUT'

        match_ip = parameters[main_key]['match ip address prefix-list']
        prefix = []
        for x in match_ip:
           if x[1] not in prefix:
                prefix.append(x[1])

        for i in range(len(prefix)):
            prefix_list = list((filter(lambda x: f"ip prefix-list {prefix[i]} " in x, core_list)))
            for z in prefix_list:
                parameters['IP_PREFIX'].append(z+'\n')