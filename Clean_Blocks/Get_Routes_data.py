import re

class Get_routes_data:

    def get_data(self, parameters, block_list, patterns):
    
        if block_list != [] and patterns['id'] == 1:
            for x in block_list:
                if re.findall('name', x):
                    x = "".join(re.findall(r'.+name', x))
                    x = x.replace('name', '').replace('ip route ', ' ').replace('vrf ', '').strip()
                    x = x.replace(parameters['INTER']['VPN'], '').strip() if parameters['INTER']['VPN'] != "" else x
                    parameters['ROUTES'].append(x)
                else:
                    x = x.replace('ip route ', ' ').replace('vrf ', '').strip()
                    x = x.replace(parameters['INTER']['VPN'], '').strip() if parameters['INTER']['VPN'] != "" else x
                    parameters['ROUTES'].append(x)

        if block_list != [] and patterns['id'] == 2:
            for x in block_list:
                if re.findall('description', x):
                    x = "".join(re.findall(r'.+description', x))
                    x = x.replace('description', '').replace('/', ' ').strip()
                    parameters['ROUTES'].append(x)
                else:
                    parameters['ROUTES'].append(x.strip())
        


        