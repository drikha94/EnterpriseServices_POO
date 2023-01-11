import re

class Get_rip_data:

    def get_data(self, block_list, parameters, patterns):
        
        def network():

            net = list(filter(lambda x: "network" in x, block_list))
            if net != []:
                parameters['RIP']['network'] = [x.replace('network', '').strip() for x in net]

        def neighbor():

            nei = list(filter(lambda x: "neighbor" in x, block_list))
            if nei != []:
                parameters['RIP']['neighbor'] = [x.replace('neighbor', '').strip() for x in nei]

        network(), neighbor()