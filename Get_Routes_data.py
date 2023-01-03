import re

class Get_routes_data:

    def __init__(self):

        self.peer = ""

    def get_data(self, parameters, block_list, peers, patterns):

        filter_routes = []
        block_list_string = "".join(block_list)

        for i in range(len(peers)):
            if re.findall(peers[i], block_list_string):
                self.peer = peers[i]
                break
        
        filter_routes = list(filter(lambda x: self.peer in x, block_list)) if self.peer != "" else []
        
        for x in filter_routes:
            if patterns['id'] == 1 and filter_routes != []:

                if re.findall('name', x):
                    x = "".join(re.findall(r'.+name', x))
                    x = x.replace('name', '').replace('ip route ', ' ').replace('vrf ', '').strip()
                    parameters['ROUTES'].append(x)
                    
                else:
                    parameters['ROUTES'].append(x.replace('ip route ', '').strip())

            if patterns['id'] == 2 and filter_routes != []:

                if re.findall('description', x):
                    x = "".join(re.findall(r'.+description', x))
                    x = x.replace('description', '').replace('/', ' ').strip()
                    parameters['ROUTES'].append(x)

                else:
                    parameters['ROUTES'].append(x.strip())
        


        