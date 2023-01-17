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

        if patterns['id'] == 1:
            for i in range(len(prefix)):
                prefix_list = list((filter(lambda x: f"ip prefix-list {prefix[i]} " in x, core_list)))
                for z in prefix_list:
                    parameters['IP_PREFIX'].append(z+'\n')
        
        if patterns['id'] == 2:
            block = []
            first_line = list((filter(lambda x: f"prefix-set {prefix[0]}" in x, core_list)))
            first_line = [x for x in first_line if x == f'prefix-set {prefix[0]}']
            if first_line != []:
                first_index = int(core_list.index(first_line[0]))
                for x in range(first_index, len(core_list)):
                    block.append(core_list[x])
                    if re.findall('!', core_list[x]):
                        break
            
            if block != []:
                num = 10
                for x in block:
                    if re.findall(r'\d+[.]\d+[.]\d+[.]\d+', x):
                        x = x.replace('/', ' ').replace(' le ', ' less-equal ').replace(',', '').strip()
                        x = f'ip ip-prefix {prefix[0]} index {num} RULE_NAME {x}\n' 
                        parameters['IP_PREFIX'].append(x)
                        num += 10
                