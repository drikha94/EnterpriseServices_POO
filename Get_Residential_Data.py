import re

class Get_residential_data:

    def get_data(self, parameters, block_list):
        
        vlan = ("".join(re.findall(r'[.]\d+', block_list[0])).replace('.', '')).strip()
        descrip = "".join(filter(lambda x: 'description ' in x, block_list)).lower()

        if re.findall('internet', descrip):
            parameters['VLAN']['TRAFFIC INTERNET'] = vlan

        if list(filter(lambda x: 'VOIP-IAD' in x, block_list)) != [] or re.findall('voip', descrip):
            parameters['VLAN']['TRAFFIC VOIP'] = vlan
        

