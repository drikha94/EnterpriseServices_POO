import re

class Get_traffic_policy:

    def get_data_policy_in(self, block_list, parameters):
        
        policy_in = re.findall(r'\d+', "".join(block_list))
        if policy_in != []:
            first_value = int(int(policy_in[0])) / 1000 
            policy_in[0] = str(int(first_value))
            parameters['POLICY_IN'] = policy_in

    def get_data_policy_out(self, block_list, parameters):

        sa = "".join(filter(lambda x: "shape" in x, block_list))
        sa = sa.replace("shape average", "").strip().split(" ")
        if sa == ['']:
            sa = "".join(filter(lambda x: "police cir" in x, block_list))
            sa = sa.replace("police cir", "").strip().split(" ")
        if sa[0].isdigit():
            parameters['POLICY_OUT']['shape average'] = str(int(int(sa[0]) / 1000))

        sp = "".join(filter(lambda x: "service-policy" in x, block_list)).replace("service-policy ", "").strip()
        parameters['POLICY_OUT']['service-policy'] = sp.replace("service-policy ", "").strip()

    def get_data_flow_queue(self, block_list, parameters):

        all_class = ['class MM','class ORO','class PLATA', 'class BRONCE','class PLATINO','class VIDEO']
        class_type = []
        class_values = []
        test = []

        for x in range(len(all_class)):
            if re.findall(all_class[x], "".join(block_list)):
                parameters['FLOW_QUEUE'][all_class[x]][0] = True

        for x in block_list:
            if re.findall("bandwidth", x) or re.findall("percent", x):
                class_values.append(int("".join(re.findall(r'\d', x))))

        for x in class_values:
            if x > 100:
                percent_value = (int((x * 100) / int(parameters['POLICY_OUT']['shape average'])))
        
            print(percent_value)

                
                    




        
        
    
