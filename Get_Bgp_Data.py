from io import open
import re

class Get_bgp_data:

    def __init__(self):

        self.bucle = 2
        self.sum_peer = [1, -1, 5, -5]
        self.possible_peers = []
        self.attributes_peer = []
        self.static_routes_service = []
        self.peer = ""

    def first_filter(self, parameters, bgp_block, patterns):

        vpn = parameters['INTER']['VPN']
        if vpn != "":

            first_line_two = list(filter(lambda x: patterns['bgp']['p_vpn'][0] + vpn in x, bgp_block))
            if first_line_two != []:
                first_line_two_string = "".join(first_line_two[0]).strip()
                if first_line_two_string == "address-family ipv4 vrf " + vpn or first_line_two_string == "vrf " + vpn:
                    confirmation = first_line_two
                else:
                    confirmation = False

        else:
            confirmation = [bgp_block[0]]

            return confirmation
        return confirmation
        

    def get_bgp_with_vpn(self, parameters, bgp_with_vpn_block):
        
        if parameters['INTER']['IP'] != "" and bgp_with_vpn_block != []:

            for peer in range(len(self.possible_peers)):
                attributes_peer = list(filter(lambda x: self.possible_peers[peer] + " " in x, bgp_with_vpn_block))

                if attributes_peer != []:
                    self.attributes_peer = attributes_peer
                    self.peer = self.possible_peers[peer]
                    

    def get_routes_with_vpn(self, parameters, block_routes):

        if parameters['INTER']['IP'] != "" and block_routes != []:

            for peer in range(len(self.possible_peers)):
                static_routes_vpn = list(filter(lambda x: parameters['INTER']['VPN'] in x, block_routes))

                if static_routes_vpn != []:
                    self.static_routes_service.append("".join(filter(lambda x: self.possible_peers[peer] in x, static_routes_vpn)))
        
        print(static_routes_vpn)
        print(self.static_routes_service)

            




                    
                

        
        



                



            


