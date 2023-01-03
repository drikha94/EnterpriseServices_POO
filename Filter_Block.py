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
        vpn = parameters['INTER']['VPN']

        if patterns['id'] == 1:

            block_list = list(filter(lambda x: 'ip route ' in x, core_list))
            if vpn != "":
                block_list_reduced = list(filter(lambda x: f'ip route vrf {vpn}' in x, block_list))
            else:
                block_list_reduced = list(filter(lambda x: f'ip route' in x if not re.findall('ip route vrf', x) else [], block_list)) 
            return block_list_reduced

        if patterns['id'] == 2:

            block_list = self.main_filter(core_list, ['router static'], data_type, '!', True)
            if vpn != "":
                first_line = list(filter(lambda x: f'vrf {vpn}' in x, block_list)) if block_list != [] else []
                block_list_reduced = self.main_filter(block_list, first_line, data_type, '!', False) if first_line != [] else []
            else:
                block_list_reduced = self.main_filter(block_list, block_list, data_type, '!', False) if block_list != [] else []
            return block_list_reduced
    
    def bgp_filter(self, parameters, patterns, core_list, peers):

        block_list = []
        data_type = 'bgp'
        vpn = parameters['INTER']['VPN']
        first_line = list((filter(lambda x: "router bgp " in x, core_list)))
        block_list_original = self.main_filter(core_list, first_line, data_type, '!', True)  if first_line != [] else []
        if block_list_original != []:
            for x in block_list_original:
                block_list.append(f'{x} ')

        if vpn == "" and block_list != []:

            if patterns['id'] == 1:
                block_list_reduced = self.main_filter(block_list, block_list, data_type, 'address-family ipv4 vrf', False)
                peer = self.peer_filter(peers, "".join(block_list_reduced))
                parameters['BGP']['PEER'] = peer
                if peer != "":
                    block_list_peer = list(filter(lambda x: f'{peer} ' in x, block_list_reduced))
                    return block_list_peer
                return []
                
            if patterns['id'] == 2:
                block_list_reduced = self.main_filter(block_list, block_list, data_type, 'vrf', False)
                peer = self.peer_filter(peers, "".join(block_list_reduced))
                parameters['BGP']['PEER'] = peer
                if peer != "":
                    first_line = list(filter(lambda x: f'{peer} ' in x, block_list_reduced))
                    block_list_peer = self.main_filter(block_list_reduced, first_line, data_type, ' ! ', True)
                    return block_list_peer
                return []


        if vpn != "" and block_list != []:

            if patterns['id'] == 1:
                first_line = list(filter(lambda x: f'address-family ipv4 vrf {vpn} ' in x, block_list))
                if first_line != []:
                    block_list_reduced = self.main_filter(block_list, first_line, data_type, '!', False)
                    peer = self.peer_filter(peers, "".join(block_list_reduced))
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
                    block_list_reduced = self.main_filter(block_list, first_line, data_type, ' ! ', True)
                    peer = self.peer_filter(peers, "".join(block_list_reduced))
                    parameters['BGP']['PEER'] = peer
                    vpn_properties = self.main_filter(block_list_reduced, block_list_reduced, data_type, '! ', False)
                    if peer != "":
                        first_line_peer = list(filter(lambda x: f'neighbor {peer} ' in x, block_list_reduced))
                        peer_properties = self.main_filter(block_list_reduced, first_line_peer, data_type, '! ', False)   
                        return peer_properties + vpn_properties
                    return vpn_properties
                return []



    def peer_filter(self, peers, block_list_string):

        peer = peers[0] if re.findall(f'{peers[0]} ', block_list_string) and peers[0] != "" else ""
        peer = peers[1] if re.findall(f'{peers[1]} ', block_list_string) and peers[1] != "" and peer == "" else peer

        if len(peers) == 4 and peer == "":
            peer = peers[2] if re.findall(f'{peers[2]} ', block_list_string) and peers[2] != "" and peer == "" else peer
            peer = peers[3] if re.findall(f'{peers[3]} ', block_list_string) and peers[3] != "" and peer == "" else peer

        return peer
        
       




            


            



        
                    
        