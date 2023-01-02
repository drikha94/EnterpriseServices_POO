import re
from tkinter import messagebox

class Filter_blocks:

    def main_filter(self, list, first_line, data_type, break_point, validation):

        block = []
        #print(first_line)
        if first_line != []:
        
            first_index = int(list.index(first_line[0]))
        
            for x in range(first_index, len(list)):

                block.append(list[x])
                if validation == False:
                    if re.findall(break_point, list[x]):
                        break
                else:
                    if re.findall(break_point, list[x]) and list[x] == break_point:
                        break
        
        else:
            messagebox.showinfo("Warning", "The legacy interface was not found")
            exit()

        return block

    def interface_filter(self, core_interface, core_list):

        data_type = 'interface'
        find_interface = list(filter(lambda linea: core_interface in linea, core_list))
        block_list = self.main_filter(core_list, find_interface, data_type, '!', True)
        return block_list

    def vpn_filter(self, parameters, patterns, core_list):

        data_type = 'vpn'
        vpn = parameters['INTER']['VPN']

        first_line = list(filter(lambda linea: patterns['vpn']['p_vpn'][0] + vpn in linea, core_list))
        if first_line == []:
            first_line = list(filter(lambda linea: patterns['vpn']['p_vpn'][1] + vpn in linea, core_list))

        block_list = self.main_filter(core_list, first_line, data_type, '!', True)

        if (block_list[0] == patterns['vpn']['p_vpn'][0] + vpn) or (block_list[0] == patterns['vpn']['p_vpn'][1] + vpn):

            if patterns['id'] == 1:
                return block_list

            if patterns['id'] == 2:
                rte_first_line = list(filter(lambda x: patterns['vpn']['p_rte'][0] in x, block_list))
                rti_first_line = list(filter(lambda x: patterns['vpn']['p_rti'][0] in x, block_list))
                rte_block_list = self.main_filter(block_list, rte_first_line, data_type, '!', False)
                rti_block_list = self.main_filter(block_list, rti_first_line, data_type, '!', False)
                return [block_list, rte_block_list, rti_block_list]

    def routes_filter(self, parameters, patterns, core_list):

        data_type = 'routes'
        vpn_block_list = []
        info_block_list = []

        if patterns['id'] == 1:
            block_list = list(filter(lambda x: patterns['routes']['p_routes'][0] in x, core_list))
            for x in block_list:
                if re.findall('ip route vrf ' + parameters['INTER']['VPN'], x) and parameters['INTER']['VPN'] != "":
                    vpn_block_list.append(x)

                if not re.findall('ip route vrf ', x) and parameters['INTER']['VPN'] == "":
                    info_block_list.append(x)
        
            return [vpn_block_list, info_block_list]

        if patterns['id'] == 2:
            block_list = self.main_filter(core_list, patterns['routes']['p_routes'], data_type, '!', True)
            for x in block_list:
                if re.findall('vrf ' + parameters['INTER']['VPN'], x) and parameters['INTER']['VPN'] != "":
                    first_line = list(filter(lambda x: 'vrf ' + parameters['INTER']['VPN'] in x, block_list))
                    vpn_block_list = self.main_filter(block_list, first_line, data_type, '!', False)

                if parameters['INTER']['VPN'] == "":
                    info_block_list = self.main_filter(block_list, block_list, data_type, '!', False)

            return [vpn_block_list, info_block_list]


            



        
                    
        