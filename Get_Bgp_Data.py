from io import open
import re

class Get_bgp_data:

    def get_data(self, parameters):

        sum_peer = [1, -1, 5, -5, 1, -1]
        possible_peers = []
        if self.parameters['INTER']['IP'] != "":

            ip_div = parameters['INTER']['IP'].split(".")
            ip_div = [int(x) for x in ip_div]

            if self.parameters['INTER']['MASK'] == "255.255.255.252":
                bucle = 2

            if self.parameters['INTER']['MASK'] == "255.255.255.248":
                bucle = 4

                for peer in range(2):
                    peers = "{}.{}.{}.{}".format(ip_div[0], ip_div[1], ip_div[2], (ip_div[3] + sum_peer[peer]))
                    possible_peers.append(peers)
            


