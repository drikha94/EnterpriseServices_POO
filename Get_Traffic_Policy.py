import re

class Get_traffic_policy:

    def get_data(self, block_list, parameters):
        
        policy_in = re.findall(r'\d+', "".join(block_list))
        if policy_in != []:
            first_value = int(int(policy_in[0])) / 1000 
            policy_in[0] = str(int(first_value))
            parameters['POLICY_IN'] = policy_in
    
